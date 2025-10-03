import os
import re
import math
import random
import time
from typing import List, Tuple

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSfdmlIVEJd0toWybkCo9xo3wIYwZZIolxO7tGi2F_3wEt9Dpg/viewform"

EV = 5.0 # Expected value of the distribution [1...6]
VAR = 0.40 # Variance of the distribution [0...2.9167]

EMAIL = os.environ.get("GFORM_EMAIL")
PASSWORD = os.environ.get("GFORM_PASS")

if not EMAIL or not PASSWORD:
    raise RuntimeError("Environment variables GFORM_EMAIL or GFORM_PASS not set!")
print(f"Using email: {EMAIL}")

def _probs_from_mu_sigma(K: int, mu: float, sigma: float) -> List[float]:
    exps = []
    for i in range(1, K + 1):
        exps.append(-((i - mu) ** 2) / (2.0 * max(sigma, 1e-6) ** 2))
    m = max(exps)
    ws = [math.exp(x - m) for x in exps]
    s = sum(ws)
    return [w / s for w in ws]

def _stats(p: List[float]) -> Tuple[float, float]:
    K = len(p)
    mean = sum((i + 1) * p[i] for i in range(K))
    var = sum(((i + 1) - mean) ** 2 * p[i] for i in range(K))
    return mean, var

def _find_mu_for_mean(K: int, sigma: float, mean_target: float, iters: int = 40) -> float:
    lo, hi = 1.0, float(K)
    for _ in range(iters):
        mid = (lo + hi) / 2.0
        p = _probs_from_mu_sigma(K, mid, sigma)
        m, _ = _stats(p)
        if m < mean_target:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0

def build_discrete_normal(K: int, mean_target: float, var_target: float,
                          mean_tol: float = 1e-3, var_tol: float = 1e-3) -> List[float]:
    """
    Return probabilities over {1..K} approximating target mean and variance.
    We bisection-search sigma; for each sigma, we bisection-search mu to hit mean.
    """
    mean_target = max(1.0, min(float(K), mean_target))

    sig_lo, sig_hi = 1e-3, 10.0

    def fit_mean_at_sigma(sigma: float) -> Tuple[List[float], float]:
        mu = _find_mu_for_mean(K, sigma, mean_target)
        p = _probs_from_mu_sigma(K, mu, sigma)
        m, v = _stats(p)
        if abs(m - mean_target) > mean_tol:
            mu += (mean_target - m) * 0.5
            mu = max(1.0, min(float(K), mu))
            p = _probs_from_mu_sigma(K, mu, sigma)
            m, v = _stats(p)
        return p, v

    p_lo, v_lo = fit_mean_at_sigma(sig_lo)
    p_hi, v_hi = fit_mean_at_sigma(sig_hi)

    if var_target <= v_lo + var_tol:
        return p_lo
    if var_target >= v_hi - var_tol:
        return p_hi

    for _ in range(40):
        sig_mid = (sig_lo + sig_hi) / 2.0
        p_mid, v_mid = fit_mean_at_sigma(sig_mid)
        if v_mid < var_target:
            sig_lo, p_lo, v_lo = sig_mid, p_mid, v_mid
        else:
            sig_hi, p_hi, v_hi = sig_mid, p_mid, v_mid
        if abs(v_mid - var_target) < var_tol:
            return p_mid

    return p_mid

driver = webdriver.Chrome()
driver.get(FORM_URL)
wait = WebDriverWait(driver, 20)

if "ServiceLogin" in driver.current_url:
    email_input = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='email']")))
    email_input.send_keys(EMAIL)
    driver.find_element(By.ID, "identifierNext").click()

    pass_input = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='password']")))
    pass_input.send_keys(PASSWORD)
    driver.find_element(By.ID, "passwordNext").click()

    wait.until(EC.url_contains("forms"))
    time.sleep(5)

print("Starting form fill...")
groups = driver.find_elements(By.XPATH, "//div[@role='radiogroup'] | //div[@role='group']")
num_parser = re.compile(r"^\s*(\d+)")

for g_idx, g in enumerate(groups, start=1):
    options = g.find_elements(By.XPATH, ".//div[@role='radio']")
    if not options:
        continue

    values = []
    for opt in options:
        label = opt.get_attribute("aria-label") or ""
        m = num_parser.match(label)
        if m:
            values.append(int(m.group(1)))
        else:
            values.append(len(values) + 1)

    K = max(values)
    probsK = build_discrete_normal(K, EV, VAR)

    opt_weights = []
    for v in values:
        if 1 <= v <= K:
            opt_weights.append(probsK[v - 1])
        else:
            opt_weights.append(1.0 / len(values))

    choice = random.choices(options, weights=opt_weights, k=1)[0]

    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", choice)
    time.sleep(0.2)
    driver.execute_script("arguments[0].click();", choice)

    print(f"Q{g_idx}: picked",
          (choice.get_attribute('aria-label') or '').split(',')[0],
          "| checked =", choice.get_attribute("aria-checked"))

print(f" Form filled with EV={EV} distribution")
print(" Browser will remain open. Press CTRL+C to stop the script.")

while True:
    time.sleep(60)
