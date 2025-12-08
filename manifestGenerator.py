import os
import random

OUT_DIR = "Additional Tests"
NUM_CASES = 20
ROWS = 8
COLS = 12
MAX_CONTAINERS = 16  # maximum number of containers per manifest

contents_list = [
    "Carpet", "Tires", "Electronics", "Tools", "Furniture",
    "Food", "Medical", "Clothing", "Machinery",
    "Batteries", "Steel", "Plastic", "Books",
    "SpareParts", "Glass", "Chemicals"]

def random_weight():
    return f"{random.randint(1, 500):05d}"

def generate_manifest():
    manifest = [[("00000", "UNUSED") for _ in range(COLS + 1)] for _ in range(ROWS + 1)]
    manifest[1][1] = ("00000", "NAN")
    manifest[1][12] = ("00000", "NAN")

    num_containers = random.randint(1, MAX_CONTAINERS)
    positions = []

    while num_containers > 0:
        if(random.randint(1,2)==2):
            c = random.randint(1, 6)

            for r in range(1, ROWS + 1):
                if manifest[r][c][1] == "UNUSED":
                    w = random.randint(50,999)
                    content = random.choice(contents_list)
                    manifest[r][c] = (f"{w:05d}", content)
                    positions.append((r, c))
                    num_containers -= 1
                    break
            if num_containers <= 0:
                break
        else:
            c = random.randint(6, COLS)
            for r in range(1, ROWS + 1):
                if manifest[r][c][1] == "UNUSED":
                    w = random.randint(50, 999)
                    content = random.choice(contents_list)
                    manifest[r][c] = (f"{w:05d}", content)
                    positions.append((r, c))
                    num_containers -= 1
                    break
        if num_containers <= 0:
            break
    return manifest

def save_manifest(manifest, filename):
    with open(filename, "w") as f:
        for r in range(1, ROWS + 1):
            for c in range(1, COLS + 1):
                weight, content = manifest[r][c]
                f.write(f"[{r:02d},{c:02d}], {{{weight}}}, {content}\n")

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    for i in range(1, NUM_CASES + 1):
        manifest = generate_manifest()
        filename = os.path.join(OUT_DIR, f"AutoTest_{i:02d}.txt")
        save_manifest(manifest, filename)
    print(f"Generated {NUM_CASES} test manifests in '{OUT_DIR}'")

if __name__ == "__main__":
    main()
