# Digital Signature App

A desktop application for **document signing, signature verification, file encryption, and RSA key generation**, built as a university project (BSK – Network Security Fundamentals) by Marcel Zieliński (191005).

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.10+ |
| GUI | `tkinter` / `ttk` |
| GUI Theme | [Azure ttk theme](https://github.com/rdbende/Azure-ttk-theme) (dark mode) |
| Asymmetric crypto | [`rsa`](https://pypi.org/project/rsa/) – RSA-4096 |
| Symmetric crypto | [`pycryptodomex`](https://pypi.org/project/pycryptodomex/) – AES-128-CBC |
| Signature format | XML (`xml.etree.ElementTree`) |

---

## Architecture

```
Digital_signature_app/
├── MainApp/
│   ├── main.py          # Core crypto logic (sign, verify, encrypt, decrypt)
│   └── main_gui.py      # tkinter GUI – entry point for the main app
├── TTP/
│   └── ttp.py           # Trusted Third Party – RSA key pair generation
├── Common/
│   ├── FrameCreator.py  # Reusable ttk frame/widget builder (builder pattern)
│   ├── globals.py       # Shared constants (key sizes, block sizes)
│   ├── helper.py        # File/directory chooser + PIN hashing logic
│   └── helper_gui.py    # GUI dialogs: LocationChooser, PinInputter
├── Azure/               # Azure ttk theme assets (azure.tcl + theme files)
└── requirements.txt
```

### Component responsibilities

- **`MainApp/main_gui.py`** – Renders a 2×2 grid of panels (Sign, Verify, Encrypt, Decrypt) and wires GUI events to `Main`.
- **`MainApp/main.py`** – Stateless crypto operations:
  - Loads RSA keys (public key from PEM; private key decrypted from AES-wrapped DER).
  - Signs a file by computing its SHA-256 hash, signing it with the private key, and saving the result as an XML file containing document metadata and the signature hex.
  - Verifies a signature by re-hashing the file and calling `rsa.verify` against the stored hex signature.
  - General-purpose RSA encrypt/decrypt for arbitrary files.
- **`TTP/ttp.py`** – Trusted Third Party utility that generates an RSA-4096 key pair. The public key is saved as PEM. The private key (DER format) is AES-128-CBC encrypted using the SHA-256 hash of a user-chosen PIN, then saved as `.pem.aes`.
- **`Common/`** – Shared infrastructure (GUI helpers, constants, hash utilities).

### Security design

| Concern | Approach |
|---|---|
| Private key storage | AES-128-CBC; IV prepended to ciphertext |
| AES key derivation | SHA-256 hash of the user PIN |
| Document hashing | SHA-256 via `rsa.compute_hash` |
| Signature algorithm | RSA-4096 + SHA-256 (`rsa.sign_hash`) |
| Signature transport | XML file containing hex-encoded signature + document metadata |

---

## Prerequisites

- Python 3.10 or newer
- Install dependencies:

```bash
pip install -r requirements.txt
```

`requirements.txt` contains:
```
pycryptodomex==3.20.0
rsa==4.9
```

---

## How to Use

### 1. Generate keys (TTP)

Run the key-generation utility once to create your RSA key pair:

```bash
cd TTP
python ttp.py
```

A dialog will ask you to choose a save directory and enter a 4-digit PIN.  
Two files are created:
- `pub.pem` – RSA public key (share freely)
- `priv.pem.aes` – RSA private key encrypted with your PIN (keep secret)

---

### 2. Launch the main application

```bash
cd MainApp
python main_gui.py
```

The window opens in dark mode and presents four panels:

| Panel | What it does |
|---|---|
| **Signing** | Browse to a file + your `priv.pem.aes`, click **Sign**. A PIN dialog appears. The signature is saved as `signature.xml` in a directory of your choice. |
| **Signature Verification** | Browse to the original file, `signature.xml`, and `pub.pem`, click **Verify**. The status field shows whether the file is original or has been modified. |
| **File Encryption** | Browse to any file + `pub.pem`, click **Encrypt**. The encrypted file is saved alongside the original with a `.rsa` extension. |
| **File Decryption** | Browse to a `.rsa` file + `priv.pem.aes`, click **Decrypt**. A PIN dialog appears and the decrypted file is restored (`.rsa` suffix removed). |

---

## Key Constants (`Common/globals.py`)

| Constant | Value | Meaning |
|---|---|---|
| `RSA_KEY_SIZE` | 4096 | RSA key length in bits |
| `AES_BLOCK_SIZE` | 16 | AES block size in bytes (128-bit) |
| `SHA_BLOCK_SIZE` | 65536 | Read chunk size for SHA hashing |
| `GUI_MODE` | 1 | GUI mode flag |
