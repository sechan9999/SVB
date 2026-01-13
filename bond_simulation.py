
import numpy as np
import matplotlib.pyplot as plt

def calculate_bond_metrics(cash_flows, yield_rate):
    """
    채권의 현재가치(PV)와 듀레이션(Duration)을 계산합니다.
    
    formula: 
    P = sum(C_i / (1+y)^i)
    Duration = (1/P) * sum(i * C_i / (1+y)^(i+1))  <- Modified Duration에 가까운 수식
    여기선 텍스트에 언급된 '현금흐름 타이밍의 가중 평균' 개념을 시각화합니다.
    """
    times = np.arange(1, len(cash_flows) + 1)
    
    # 1. 각 시점별 현금흐름의 현재가치(PV) 계산
    pvs = [c / (1 + yield_rate)**t for t, c in zip(times, cash_flows)]
    total_p = sum(pvs)
    
    # 2. 가중치(Weights) 계산: w_i = PV_i / Total_P
    weights = [pv / total_p for pv in pvs]
    
    # 3. 듀레이션 계산 (무게 중심)
    # 텍스트의 수식에 따라 (1/(1+y)) * sum(w_i * i) 계산
    duration = (1 / (1 + yield_rate)) * sum(w * t for w, t in zip(weights, times))
    
    return total_p, pvs, duration

def plot_bond_plank(name, cash_flows, yield_rate, ax):
    """
    채권의 현금흐름을 널빤지 위의 무게추로 시각화합니다.
    """
    price, pvs, duration = calculate_bond_metrics(cash_flows, yield_rate)
    times = np.arange(1, len(cash_flows) + 1)
    
    # 널빤지 그리기
    ax.axhline(0, color='black', linewidth=2)
    
    # 무게추(PV) 그리기
    ax.bar(times, pvs, width=0.4, color='skyblue', alpha=0.7, label='PV of Cashflows')
    
    # 무게 중심(Duration) 표시
    ax.plot(duration, 0, '^', color='red', markersize=15, label=f'Duration: {duration:.2f} yrs')
    ax.annotate('Center of Mass\n(Duration)', xy=(duration, 0), xytext=(duration, max(pvs)*0.5),
                arrowprops=dict(facecolor='black', shrink=0.05),
                horizontalalignment='center')

    ax.set_title(f"{name} (Price: ${price:,.0f})")
    ax.set_xlabel("Time (Years)")
    ax.set_ylabel("Present Value ($)")
    ax.grid(True, axis='y', linestyle='--', alpha=0.6)
    ax.legend()

def run_simulation():
    # 시뮬레이션 설정
    T = 20  # 20년 만기
    yield_rate = 0.05  # 5% 금리
    face_value = 1000000  # 원금 100만 달러
    coupon_rate = 0.04  # 쿠폰 4%
    
    # 1. 일반 국채 (Treasury Bond): 매년 이자만 주다가 마지막에 원금 상환
    treasury_cfs = [face_value * coupon_rate] * T
    treasury_cfs[-1] += face_value
    
    # 2. 모기지 채권 (Mortgage Bond): 원리금 균등 상환 (매년 동일한 금액 지불)
    # 원리금 균등 상환액 계산 공식: A = P * r * (1+r)^n / ((1+r)^n - 1)
    r = 0.04 # 대출 이자율
    annuity = face_value * r * (1+r)**T / ((1+r)**T - 1)
    mortgage_cfs = [annuity] * T

    # 시각화
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    plot_bond_plank("Treasury Bond (Bullet Repayment)", treasury_cfs, yield_rate, ax1)
    plot_bond_plank("Mortgage Bond (Amortized)", mortgage_cfs, yield_rate, ax2)
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    run_simulation()
