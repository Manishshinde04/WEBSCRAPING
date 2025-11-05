# PricePulse - Live Amazon Price Tracker 🚀

![Project Status](https://img.shields.io/badge/status-active-brightgreen?style=for-the-badge)
![License](https://img.shields.io/badge/license-MIT-blue?style=for-the-badge)

A real-time Amazon product price tracker built with a Python (Flask) backend and an HTML/JavaScript frontend. This application scrapes product data on-demand and displays it on a dynamic dashboard with live price-history charts.

---

## 📸 Demo

> **Note:** Replace this static image with an animated GIF!
> A great free tool for this is [ScreenToGif](https://www.screentogif.com/). Just record your screen showing the app load, then tracking a new product.
https://drive.google.com/drive/folders/13F6WHZ484ucAfSr5gkxWjE16hvYhaQei
---

## 🛠 Tech Stack

This project uses a modern, simple tech stack:

### **Backend**
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![Beautiful Soup](https://img.shields.io/badge/Beautiful%20Soup-404040?style=for-the-badge&logo=python&logoColor=white)

### **Frontend**
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind%20CSS-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![Chart.js](https://img.shields.io/badge/Chart.js-FF6384?style=for-the-badge&logo=chartdotjs&logoColor=white)

---

## ✨ Core Features

* **✨ Real-Time Scraping:** Fetches product name, image, and price directly from the URL.
* **🌍 Multi-Domain Support:** Works with both `Amazon.com` (USD) and `Amazon.in` (INR).
* **💸 Automatic Price Conversion:** All prices are automatically converted to and displayed in **INR (₹)**.
* **📈 Live Price-History Charts:** Generates a live chart for each product to track its price over time.
* **⚡ Dynamic Dashboard:** Products are added to the UI instantly without a page refresh, complete with animations.
* **💾 Persistent Data:** All tracked products are saved to `product_data.json` so your dashboard is reloaded on page-load.

---

## 🚀 How to Run This Project

Follow these instructions to get the project up and running on your local machine.

### **Prerequisites**

* You must have [Python 3.7+](https://www.python.org/downloads/) installed.
* You must have [Git](https://git-scm.com/downloads) installed.

### **1. Clone the Repository**

Open your terminal and clone this project:
```bash
git clone [https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git)
cd YOUR_REPOSITORY_NAME
