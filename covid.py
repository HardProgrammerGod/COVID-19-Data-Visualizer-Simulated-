import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Simulate data
def simulate_data(days=100):
    dates = pd.date_range(end=pd.Timestamp.today(), periods=days)
    np.random.seed(42)
    new_cases = np.random.poisson(lam=800, size=days) + np.random.randint(-100, 100, size=days)
    new_cases = np.clip(new_cases, 0, None)
    new_deaths = (new_cases * np.random.uniform(0.01, 0.05, size=days)).astype(int)

    df = pd.DataFrame({
        'date': dates,
        'new_cases': new_cases,
        'new_deaths': new_deaths
    })
    df['7_day_avg'] = df['new_cases'].rolling(window=7).mean()
    df['week'] = df['date'].dt.isocalendar().week
    return df

# Plot functions
def plot_cases(df):
    plt.figure(figsize=(10, 5))
    plt.plot(df['date'], df['new_cases'], label='Daily Cases', alpha=0.6)
    plt.plot(df['date'], df['7_day_avg'], label='7-day Avg', color='red')
    plt.title("Daily Cases with 7-Day Moving Average")
    plt.xlabel("Date")
    plt.ylabel("Cases")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

def plot_weekly(df):
    weekly = df.groupby('week').sum(numeric_only=True)
    plt.figure(figsize=(10, 5))
    plt.bar(weekly.index, weekly['new_cases'], color='purple')
    plt.title("Weekly Total Cases")
    plt.xlabel("Week Number")
    plt.ylabel("Cases")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_dual_axis(df):
    fig, ax1 = plt.subplots(figsize=(10, 5))
    ax1.plot(df['date'], df['new_cases'], color='blue', label='Cases')
    ax1.set_xlabel("Date")
    ax1.set_ylabel("New Cases", color='blue')

    ax2 = ax1.twinx()
    ax2.plot(df['date'], df['new_deaths'], color='red', label='Deaths')
    ax2.set_ylabel("New Deaths", color='red')

    plt.title("Cases vs Deaths")
    fig.tight_layout()
    plt.grid(True)
    plt.show()

# GUI setup
def run_gui(df):
    root = tk.Tk()
    root.title("COVID-19 Dashboard (Simulated)")
    root.geometry("300x250")
    root.resizable(False, False)

    ttk.Label(root, text="COVID-19 Data Viewer", font=("Arial", 14)).pack(pady=20)

    ttk.Button(root, text="📈 Daily Cases (7-day avg)", command=lambda: plot_cases(df)).pack(pady=5)
    ttk.Button(root, text="📊 Weekly Summary", command=lambda: plot_weekly(df)).pack(pady=5)
    ttk.Button(root, text="📉 Cases vs Deaths", command=lambda: plot_dual_axis(df)).pack(pady=5)
    ttk.Button(root, text="❌ Exit", command=root.destroy).pack(pady=20)

    root.mainloop()

# Run it
if __name__ == '__main__':
    df = simulate_data()
    run_gui(df)
