from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
# print(f'This is the base dir: {BASE_DIR}')
ARTIFACT_DIR = BASE_DIR/"artifacts"
# print(f'This is the artifact dir: {ARTIFACT_DIR}')