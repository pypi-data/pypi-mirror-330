
### **README.md**

# **vaspc**

*A lightweight package for VASP input file generation.*

---

## **✨ Overview**

`vaspc` is a simple and efficient tool designed to assist users in generating **VASP input files** (`POTCAR`, `INCAR`, `POSCAR`) with minimal effort. It automates file conversion, potential selection, and input parameter setup, making it easier to prepare computational chemistry simulations.

---

## **🚀 Installation**

```bash
pip install vaspc
```

Ensure that `vaspc` is installed in your Python environment before proceeding.

---

## **📌 Usage**

### **Step 1: Navigate to the Directory Containing Your CIF File**

```bash
cd /path/to/your/cif/files
```

### **Step 2: Run `vaspc`**

```bash
vaspc
```

This will automatically:

* Convert your CIF file to **POSCAR**
* Generate an optimized **INCAR**
* Assemble the required **POTCAR**

---

## **🔧 Features**

✅ **Automatic CIF to POSCAR conversion**
✅ **Interactive POTCAR selection (if needed)**
✅ **Predefined INCAR templates for different calculation types**
✅ **Simple CLI-based execution**

---

## **📂 File Output**

After running `vaspc`, you will get the following files in your working directory:

###### /your/cif/files/
│── POSCAR
│── INCAR
│── POTCAR

These files are ready to be used in VASP calculations.

---

## **⚙ Dependencies**

`vaspc` requires the following packages:

* [`ase`]() (Atomic Simulation Environment)

Dependencies are automatically installed with `pip install vaspc`.

---

## **👨‍💻 Contributing**

We welcome contributions! If you find a bug or have an idea for improvement, feel free to submit an issue or a pull request.

---

## **📄 License**

This project is licensed under the  **MIT License** .
