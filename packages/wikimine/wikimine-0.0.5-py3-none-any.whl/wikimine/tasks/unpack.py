import bz2
import json
import os
from tqdm import tqdm


def split_wikidata_dump(input_file, output_folder, batch_size=1000, stop_at=-1):
    """
    Split a Wikidata JSON.bz2 dump into smaller JSONL.bz2 files.

    Parameters:
    - input_file: str, path to the input Wikidata JSON.bz2 dump file.
    - output_prefix: str, prefix for the output files.
    - batch_size: int, number of entities in each batch file.
    """

    os.makedirs(output_folder, exist_ok=True)

    def write_batch_to_file(batch, batch_num):
        """Write a batch of entities to a compressed JSONL.bz2 file."""
        output_file = os.path.join(output_folder, f"{batch_num:012d}.jsonl.bz2")
        with bz2.open(output_file, 'wt') as bz2_file:
            for entity in batch:
                bz2_file.write(json.dumps(entity) + '\n')

    batch = []
    batch_num = 0

    count = 0

    with bz2.open(input_file, 'rt') as bz2_file:
        for line in tqdm(bz2_file):
            if line.startswith('[') or line.startswith(']'):
                # Skip the starting and ending brackets of the JSON array
                continue
            count += 1

            if stop_at >= 0 and count > stop_at:
                break

            # Remove the trailing comma if it's not the last line
            if line.endswith(',\n'):
                line = line[:-2] + '\n'

            # Parse the line as JSON
            entity = json.loads(line)

            batch.append(entity)

            # If batch size is reached, write the batch to a file
            if len(batch) >= batch_size:
                write_batch_to_file(batch, batch_num)
                batch = []
                batch_num += 1

    # Write the remaining batch if any
    if batch:
        write_batch_to_file(batch, batch_num)

    print(f"Splitting completed. {batch_num + 1} batch files created.")
