# Where2Surf

## 🌊 Overview

This project uses a **forked version** of the [`pysurfline`](https://github.com/Mircobrb/pysurfline) package to access surf data from the Surfline API. It fetches surf forecast data for given spot IDs and structures the output into a clean **Pandas DataFrame**, making it easy to analyze and manipulate.

This work is partially inspired by [Justin Gosses' Surfline API exploration](https://observablehq.com/@justingosses/surfline-api-exploration), which helped uncover how to interact with the API endpoints effectively.

---

## 📦 Installation

### Step 1: Install the forked `pysurfline` package

#### Option A: Using HTTPS

```bash
pip install git+https://github.com/Mircobrb/pysurfline.git
```

#### Option B: Using SSH (requires GitHub SSH access)

```bash
pip install git+ssh://git@github.com/Mircobrb/pysurfline.git
```

---

### Step 2: Install additional dependencies

Make sure you're in the root directory of this project, then run:

```bash
pip install -r requirements.txt
```

---

## 🙌 Credits

- This project uses a **forked version** of [`pysurfline`](https://github.com/Mircobrb/pysurfline) by [@Mircobrb](https://github.com/Mircobrb), originally based on the work by [@wolfinger](https://github.com/wolfinger/pysurfline).
- API exploration reference: [Surfline API Exploration by Justin Gosses](https://observablehq.com/@justingosses/surfline-api-exploration).

---

Let me know if you also want to pin a specific commit or tag when installing from the fork, or if you want to add usage instructions!