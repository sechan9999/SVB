
import numpy as np
import matplotlib.pyplot as plt
import argparse
import os
import sys

def calculate_bond_metrics(cash_flows, yield_rate):
    """
    Calculates the Present Value (PV) and Duration of a bond.
    
    Formula: 
    P = sum(C_i / (1+y)^i)
    Duration = (1/P) * sum(i * C_i / (1+y)^(i+1))  <- Close to Modified Duration
    This visualizes the concept of 'weighted average of cash flow timing' mentioned in the text.
    """
    times = np.arange(1, len(cash_flows) + 1)
    
    # 1. Calculate PV of cash flows for each period
    pvs = [c / (1 + yield_rate)**t for t, c in zip(times, cash_flows)]
    total_p = sum(pvs)
    
    # 2. Calculate Weights: w_i = PV_i / Total_P
    weights = [pv / total_p for pv in pvs]
    
    # 3. Calculate Duration (Center of Mass)
    # Calculation according to the formula: (1/(1+y)) * sum(w_i * i)
    duration = (1 / (1 + yield_rate)) * sum(w * t for w, t in zip(weights, times))
    
    return total_p, pvs, duration

def plot_bond_plank(name, cash_flows, yield_rate, ax):
    """
    Visualizes the bond's cash flows as weights on a plank.
    """
    price, pvs, duration = calculate_bond_metrics(cash_flows, yield_rate)
    times = np.arange(1, len(cash_flows) + 1)
    
    # Draw the plank
    ax.axhline(0, color='black', linewidth=2)
    
    # Draw weights (PV)
    ax.bar(times, pvs, width=0.4, color='skyblue', alpha=0.7, label='PV of Cashflows')
    
    # Mark Center of Mass (Duration)
    ax.plot(duration, 0, '^', color='red', markersize=15, label=f'Duration: {duration:.2f} yrs')
    ax.annotate('Center of Mass\n(Duration)', xy=(duration, 0), xytext=(duration, max(pvs)*0.5),
                arrowprops=dict(facecolor='black', shrink=0.05),
                horizontalalignment='center')

    ax.set_title(f"{name} (Price: ${price:,.0f})")
    ax.set_xlabel("Time (Years)")
    ax.set_ylabel("Present Value ($)")
    ax.grid(True, axis='y', linestyle='--', alpha=0.6)
    ax.legend()

def run_simulation(T, yield_rate, face_value, coupon_rate, output_dir):
    # 1. Treasury Bond (Bullet Repayment): Interest only every year, principal at the end
    treasury_cfs = [face_value * coupon_rate] * T
    treasury_cfs[-1] += face_value
    
    # 2. Mortgage Bond (Amortized): Equal principal and interest repayment (same amount paid every year)
    # Formula for amortized repayment: A = P * r * (1+r)^n / ((1+r)^n - 1)
    r = 0.04 # Loan interest rate (assumed same as coupon rate concept here for simplicity)
    annuity = face_value * r * (1+r)**T / ((1+r)**T - 1)
    mortgage_cfs = [annuity] * T

    # Visualization
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    plot_bond_plank("Treasury Bond (Bullet Repayment)", treasury_cfs, yield_rate, ax1)
    plot_bond_plank("Mortgage Bond (Amortized)", mortgage_cfs, yield_rate, ax2)
    
    # Print Results
    t_price, _, t_dur = calculate_bond_metrics(treasury_cfs, yield_rate)
    m_price, _, m_dur = calculate_bond_metrics(mortgage_cfs, yield_rate)
    
    print("-" * 50)
    print(f"1. Treasury Bond (Bullet)")
    print(f"   - Price:    ${t_price:,.2f}")
    print(f"   - Duration: {t_dur:.4f} years")
    
    print("-" * 50)
    print(f"2. Mortgage Bond (Amortized)")
    print(f"   - Price:    ${m_price:,.2f}")
    print(f"   - Duration: {m_dur:.4f} years")
    print("-" * 50)

    # Save to file
    output_path = os.path.join(output_dir, 'svb_duration_analysis.png')
    try:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        plt.savefig(output_path)
        print(f"\nGraph saved to: {output_path}")
    except Exception as e:
        print(f"\nError saving graph to {output_path}: {e}", file=sys.stderr)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bond Duration Simulation")
    parser.add_argument("--T", type=int, default=20, help="Maturity in years (default: 20)")
    parser.add_argument("--yield_rate", type=float, default=0.05, help="Yield rate (default: 0.05)")
    parser.add_argument("--face_value", type=float, default=1000000, help="Face value (default: 1,000,000)")
    parser.add_argument("--coupon_rate", type=float, default=0.04, help="Coupon rate (default: 0.04)")
    parser.add_argument("--output_dir", type=str, default=".", help="Directory to save the output image (default: current directory)")

    args = parser.parse_args()

    run_simulation(args.T, args.yield_rate, args.face_value, args.coupon_rate, args.output_dir)
