# IoT Internship at SKITM&G, Jaipur

Welcome to the resource repository for the IoT Product Design Workshop held at the **Center of Excellence in IoT, SKITM&G, Jaipur**. This repository contains all the necessary files, code, and guides to build the IoT project from scratch.



## 📋 Table of Contents

1.  [Project Overview](#-project-overview)
2.  [The Workflow](#-the-workflow)
    * [Step 1: Simulation in WokWi](#-step-1-simulation-in-wokwi)
    * [Step 2: Hardware & PCB Design in EasyEDA](#-step-2-hardware--pcb-design-in-easyeda)
    * [Step 3: Firmware Development with MicroPython](#-step-3-firmware-development-with-micropython)
3.  [Repository Structure](#-repository-structure)
4.  [Essential Resources](#-essential-resources)
5.  [Acknowledgements](#-acknowledgements)

---

## 🎯 Project Overview

This project is a hands-on introduction to designing a complete IoT product. The goal was to build a simple **AI Powered IoT Environmental Monitor** using an **ESP32** microcontroller. It demonstrates the full lifecycle of product development: from digital simulation to a physical, custom-designed PCB with real-world firmware.

**Key Features:**
* Reads sensor data (e.g., temperature, humidity).
* Programmed using **MicroPython**, an easy-to-learn Python implementation for microcontrollers.
* Custom-designed PCB for a clean and robust final product.

---

## 🚀 The Workflow

We followed a 3-step process to take our idea from concept to reality.

### 🔌 Step 1: Simulation in WokWi

Before touching any physical hardware, we simulated the entire circuit and tested our initial code using the WokWi online simulator. This is a crucial step to validate the design and logic.

* **Find the simulation files in:** `1_Simulation_Wokwi/`
* **Or view the live project on Wokwi:** `[Link to your public Wokwi project]`

### 🛠️ Step 2: Hardware & PCB Design in EasyEDA

Once the simulation was successful, we designed a custom Printed Circuit Board (PCB) to house our components. This gives the project a professional and permanent form factor.

* **PCB project files are in:** `2_Hardware_EasyEDA/project_files/`
* **Gerber files for manufacturing are in:** `2_Hardware_EasyEDA/gerbers/`

### 💻 Step 3: Firmware Development with MicroPython

With the physical hardware ready, the final step is to flash the ESP32 with the MicroPython firmware and upload our application script.

1.  **Flash MicroPython Firmware:** If your ESP32 is new, you first need to install the base MicroPython firmware. You can find instructions [here](https://docs.micropython.org/en/latest/esp32/tutorial/intro.html).
2.  **Upload the Project Code:** Use a tool like Thonny IDE to upload the `main.py` and `boot.py` files from the `3_Firmware_Micropython/` directory to your ESP32.

---

## 📂 Repository Structure

* `1_Simulation_Wokwi/`: Contains `wokwi.toml` and `diagram.json` for the online simulation.
* `2_Hardware_EasyEDA/`: Contains schematic, PCB, and Gerber files.
* `3_Firmware_Micropython/`: Contains the MicroPython source code (`main.py`).
* `4_Resources/`: Contains the workshop presentation, component datasheets, and other useful links.

---

## 📚 Essential Resources

* **Workshop Presentation:** The complete presentation can be found in `4_Resources/presentation/`.
* **Datasheets:** Key component datasheets are located in `4_Resources/datasheets/`.
* **Useful Links:** A list of online calculators (like the Digikey resistor calculator), component suppliers, and other helpful sites is available in `4_Resources/useful_links.md`.

---

## 🙏 Acknowledgements

A special thank you to the **SKITM&G, Jaipur**, for hosting this workshop and supporting the next generation of IoT engineers.

---

## 📄 License

This project is open-source and licensed under the **MIT License**. See the `LICENSE` file for more details.
