class BinaryFileSplitterEditor:
    def __init__(self, file_path, split_size):
        self.file_path = file_path
        self.split_size = split_size
        self.chunks = []
        self.original_chunks = {}

    def split_file(self):
        with open(self.file_path, 'rb') as f:
            chunk_num = 0
            while True:
                chunk = f.read(self.split_size)
                if not chunk:
                    break
                chunk_file = f"{self.file_path}_chunk_{chunk_num:04d}.bin"
                with open(chunk_file, 'wb') as chunk_f:
                    chunk_f.write(chunk)
                self.chunks.append(chunk_file)
                # Store original chunk data for comparison
                self.original_chunks[chunk_num] = chunk
                chunk_num += 1
        print(f"File has been split into {len(self.chunks)} chunks.\n")

    def edit_chunk(self, chunk_index, offset, hex_data):
        if 0 <= chunk_index < len(self.chunks):
            chunk_file = self.chunks[chunk_index]
            original_chunk = self.original_chunks[chunk_index]

            # Convert hex string to bytes
            data = bytes.fromhex(hex_data)

            with open(chunk_file, 'r+b') as f:
                f.seek(offset)
                old_data = f.read(len(data))
                f.seek(offset)
                f.write(data)

            print(f"\nChunk {chunk_index} modified at offset {offset}.")
            print(f"Original data (hex): {old_data.hex()}")
            print(f"New data (hex): {data.hex()}\n")

            # Show the original and modified chunk differences
            self.show_diff(original_chunk, chunk_file, offset, data)
        else:
            print(f"Error: Chunk {chunk_index} does not exist.\n")

    def show_diff(self, original_chunk, chunk_file, offset, new_data):
        print("Difference in chunk around the modified area:")
        print(f"{'Original Data':<20} | {'New Data':<20}")
        print("-" * 45)

        original_hex = original_chunk[offset:offset + len(new_data)].hex()
        new_hex = new_data.hex()
        for i in range(0, len(original_hex), 2):
            print(f"{original_hex[i:i + 2]:<20} | {new_hex[i:i + 2]:<20}")
        print("\n")

    def merge_chunks(self, output_file):
        with open(output_file, 'wb') as f:
            for chunk_file in self.chunks:
                with open(chunk_file, 'rb') as chunk_f:
                    f.write(chunk_f.read())
        print(f"All chunks have been merged into {output_file}.\n")

    def interactive_edit(self):
        while True:
            print("\nCurrent Chunks Available:")
            for i, chunk in enumerate(self.chunks):
                print(f"{i}: {chunk}")

            chunk_index = int(
                input("\nEnter the index number of the chunk you want to edit (or enter -1 to finish editing): "))
            if chunk_index == -1:
                break

            offset = int(input(
                "Enter the position (offset) in the chunk where you want to start editing (e.g., 0 for the beginning): "))
            hex_data = input("Enter the new data (as a hex string, e.g., '4e657764'): ")

            self.edit_chunk(chunk_index, offset, hex_data)


if __name__ == "__main__":
    print("Binary File Splitter and Editor\n")
    file_path = 'test.bin'  # Update with your binary file name
    split_size = 1024 * 1024  # 1 MB per chunk

    splitter_editor = BinaryFileSplitterEditor(file_path, split_size)

    print(f"Splitting file '{file_path}' into chunks of {split_size} bytes each...\n")
    splitter_editor.split_file()

    print("Now, let's edit the chunks.")
    splitter_editor.interactive_edit()

    print("Merging the edited chunks back into a single file 'merged_test.bin'...\n")
    splitter_editor.merge_chunks('merged_test.bin')
    print("Process completed.")
