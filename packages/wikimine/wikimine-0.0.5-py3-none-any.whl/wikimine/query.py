from dataclasses import dataclass
from typing import Union
from collections import Counter
from .extractor import Aggregator, ClaimExtractor
from .db import WikidataClaim
from .labels import lookup_label
from .relations import TypingRelations


def get_label(eid):
    label = lookup_label(eid)
    if label == eid:
        return label
    else:
        return f"{eid}:{label}"


class TreeResult:
    def __init__(self, root_id: str):
        self.root_id = root_id
        self.children: list['TreeResult'] = []

    def to_dict(self, fetch_label=True) -> dict:
        item = {
            "root_id": self.root_id,
            "children": [child.to_dict() for child in self.children]
        }

        if fetch_label:
            item["label"] = get_label(self.root_id)

        return item

    def __repr__(self) -> str:
        """
        Returns a string representation of the tree using indentation.
        """
        return self._repr_helper()

    def _repr_helper(self, level: int = 0, is_last: bool = True, fetch_label=False) -> str:
        label = get_label(self.root_id) if fetch_label else self.root_id

        prefix = "    " * (level - 1) + ("└── " if is_last and level > 0 else "├── " if level > 0 else "")
        result = f"{prefix}{label}\n"

        for idx, child in enumerate(self.children):
            is_last_child = idx == len(self.children) - 1
            result += child._repr_helper(level + 1, is_last_child, fetch_label)

        return result

    def show(self):
        return print(self._repr_helper(fetch_label=True))

    def flatten(self) -> list[str]:
        """
        Flattens the tree into a list of root_ids using preorder traversal.
        :return: List of all node root_ids.
        """
        flat_list = []

        def _flatten(node: 'TreeResult'):
            flat_list.append(node.root_id)
            for child in node.children:
                _flatten(child)

        _flatten(self)
        return flat_list


def get_tree(root: str, prop_id: str, direction='forward') -> TreeResult:
    """
    Entry point for building the tree. Initializes visited set.
    """
    if direction not in ['forward', 'backward']:
        raise ValueError('direction must be either "forward" or "backward"')
    visited = set()
    if isinstance(prop_id, str):
        prop_id = [prop_id]
    return _build_tree(root, prop_id, visited, direction)


def _build_tree(root: str, prop_id: list[str], visited: set[str], direction) -> TreeResult:
    """
    Auxiliary recursive function to build the tree.
    """
    if root in visited:
        # Prevent infinite loops in case of cyclic references
        return TreeResult(root)

    visited.add(root)
    tree = TreeResult(root)

    # Get immediate children
    children = list_neighbors(root, prop_id, direction)

    # Recursively process each child
    for child_id in children:
        child_tree = _build_tree(child_id, prop_id, visited, direction)
        tree.children.append(child_tree)

    return tree


def list_neighbors(root: str, prop_id: Union[list[str], str], direction) -> list[str]:
    if isinstance(prop_id, str):
        prop_id = [prop_id]

    if direction == 'forward':
        query = WikidataClaim.select().where(
            WikidataClaim.source_entity == root,
            WikidataClaim.property_id.in_(prop_id),
        )
        return [
            item.target_entity for item in query
        ]

    elif direction == 'backward':
        query = WikidataClaim.select().where(
            (WikidataClaim.target_entity == root) &
            (WikidataClaim.property_id.in_(prop_id))
        )
        return [
            item.source_entity for item in query
        ]

    else:
        return []


def get_profile(entity: str, props: list[str] = None, resolve_target=None):
    if resolve_target is None:
        resolve_target = {}

    filters = [
        WikidataClaim.source_entity == entity,
    ]

    if props is not None and len(props) > 0:
        filters.append(WikidataClaim.property_id.in_(props))

    query = WikidataClaim.select().where(
        **filters,
    )

    profile = {

    }

    for claim in query:
        if claim.property_id not in profile:
            profile[claim.property_id] = []

        post_process_fn = resolve_target.get(
            claim.property_id,
            ClaimExtractor.get_target_label_and_id
        )

        profile[claim.property_id].append(
            post_process_fn(claim.target_entity)
        )

    return profile


def get_classes_of_instance(source_entity):
    ns = list_neighbors(source_entity, TypingRelations.instance_of, 'forward')
    return ns


def get_common_classes(source_entity_list):
    cc = Counter()
    for e in source_entity_list:
        clzs = get_classes_of_instance(e)
        cc.update(clzs)
    ret = []
    for clz, count in cc.most_common():
        ret.append(ret.append(
            LabelCount(label=lookup_label(clz), entity=clz, count=count)
        ))
    return ret


def list_instances_of(clz, limit=50):
    if isinstance(clz, str):
        clz = [clz]

    query = WikidataClaim.select().where(
        WikidataClaim.property_id == 'P31',
        WikidataClaim.target_entity.in_(clz),
    )

    if limit > 0:
        query = query.limit(limit)

    return list(query)


def get_all_out_going_edges(root):
    query = WikidataClaim.select().where(
        WikidataClaim.source_entity == root,
    )
    return list(query)


def get_common_edges(clz, limit=50):
    instances = list_instances_of(clz, limit=limit)
    edge_counter = Counter()
    for instance in instances:
        out_edges = get_all_out_going_edges(instance.source_entity)
        out_edges = list({e.property_id for e in out_edges})
        edge_counter.update(out_edges)
    ret = []
    for clz, count in edge_counter.most_common():
        ret.append(
            LabelCount(label=lookup_label(clz), entity=clz, count=count)
        )
    return LabelCountList(counts=ret, total=len(instances))


@dataclass
class LabelCount:
    label: str
    entity: str
    count: int

    def to_dict(self):
        return {
            'label': self.label,
            'entity': self.entity,
            'count': self.count,
        }

    def __repr__(self):
        return f'{self.label} - {self.entity}: {self.count}'

    def __str__(self):
        return f'{self.label} - {self.entity}: {self.count}'


@dataclass
class LabelCountList:
    counts: list[LabelCount]
    total: int

    def print_summary(self, cutoff=0.8):
        cutoff = int(cutoff * self.total)
        for label in self.counts:
            if label.count >= cutoff:
                print(f'{label.label} - {label.entity}: {label.count}/{self.total}')
