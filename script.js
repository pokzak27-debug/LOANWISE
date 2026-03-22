/**
 * LoanWise - Loan Calculator
 * Supports multiple currencies.
 * Optimized to avoid forced layout and reduce main-thread blocking.
 */

const CURRENCIES = ['USD', 'EUR', 'GBP', 'MAD', 'CAD', 'AUD', 'CHF', 'JPY', 'AED'];

document.addEventListener('DOMContentLoaded', () => {
  // Defer init to avoid blocking LCP; use idle callback with fallback
  const run = () => requestAnimationFrame(initCalculator);
  if ('requestIdleCallback' in window) {
    requestIdleCallback(run, { timeout: 80 });
  } else {
    requestAnimationFrame(run);
  }
});

function initCalculator() {
  // Early bailout for pages without calculator (about, contact, etc.)
  const currencySelect = document.getElementById('currency');
  if (!currencySelect) return;

  const loanAmountInput = document.getElementById('loanAmount');
  const interestRateInput = document.getElementById('interestRate');
  const loanTermInput = document.getElementById('loanTerm');
  const calculateBtn = document.getElementById('calculateBtn');
  const monthlyPaymentOutput = document.getElementById('monthlyPayment');
  const totalPaymentOutput = document.getElementById('totalPayment');
  const totalInterestOutput = document.getElementById('totalInterest');

  function calculateMonthlyPayment(principal, annualRate, months) {
    if (principal <= 0 || months <= 0) return null;
    const monthlyRate = annualRate / 100 / 12;
    if (monthlyRate === 0) return principal / months;
    const factor = Math.pow(1 + monthlyRate, months);
    return (principal * monthlyRate * factor) / (factor - 1);
  }

  function formatCurrency(amount, currency) {
    const validCurrency = CURRENCIES.includes(currency) ? currency : 'USD';
    const options = {
      style: 'currency',
      currency: validCurrency,
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    };
    if (validCurrency === 'JPY') {
      options.minimumFractionDigits = 0;
      options.maximumFractionDigits = 0;
    }
    return new Intl.NumberFormat('en-US', options).format(amount);
  }

  function validateInput(value, min, max, isFloat) {
    const parsed = isFloat ? parseFloat(value) : parseInt(value, 10);
    if (isNaN(parsed)) return { valid: false, value: null };
    if (min !== undefined && parsed < min) return { valid: false, value: null };
    if (max !== undefined && parsed > max) return { valid: false, value: null };
    return { valid: true, value: parsed };
  }

  // Batched DOM writes: all textContent first, then all classList, to avoid read-write interleaving
  function clearResults() {
    if (monthlyPaymentOutput) monthlyPaymentOutput.textContent = '—';
    if (totalPaymentOutput) totalPaymentOutput.textContent = '—';
    if (totalInterestOutput) totalInterestOutput.textContent = '—';
    if (monthlyPaymentOutput) monthlyPaymentOutput.classList.remove('has-value');
    if (totalPaymentOutput) totalPaymentOutput.classList.remove('has-value');
    if (totalInterestOutput) totalInterestOutput.classList.remove('has-value');
  }

  // Batched DOM writes: all textContent first, then all classList, to avoid layout thrashing
  function setResults(monthly, total, interest, currency) {
    const monthlyStr = formatCurrency(monthly, currency);
    const totalStr = formatCurrency(total, currency);
    const interestStr = formatCurrency(interest, currency);

    if (monthlyPaymentOutput) monthlyPaymentOutput.textContent = monthlyStr;
    if (totalPaymentOutput) totalPaymentOutput.textContent = totalStr;
    if (totalInterestOutput) totalInterestOutput.textContent = interestStr;
    if (monthlyPaymentOutput) monthlyPaymentOutput.classList.add('has-value');
    if (totalPaymentOutput) totalPaymentOutput.classList.add('has-value');
    if (totalInterestOutput) totalInterestOutput.classList.add('has-value');
  }

  function handleCalculate() {
    const principalResult = validateInput(loanAmountInput.value, 1, undefined, true);
    const rateResult = validateInput(interestRateInput.value, 0, 100, true);
    const monthsResult = validateInput(loanTermInput.value, 1, 600, false);

    if (!principalResult.valid || !monthsResult.valid) {
      clearResults();
      return;
    }

    const principal = principalResult.value;
    const annualRate = rateResult.valid ? rateResult.value : 0;
    const months = monthsResult.value;
    const currency = currencySelect.value;

    const payment = calculateMonthlyPayment(principal, annualRate, months);
    if (payment === null || !isFinite(payment)) {
      clearResults();
      return;
    }

    const totalPayment = payment * months;
    const totalInterest = totalPayment - principal;

    setResults(payment, totalPayment, totalInterest, currency);
  }

  function onEnterKey(e) {
    if (e.key === 'Enter') {
      e.preventDefault();
      handleCalculate();
    }
  }

  if (calculateBtn) calculateBtn.addEventListener('click', handleCalculate);

  const formInputs = [currencySelect, loanAmountInput, interestRateInput, loanTermInput];
  for (let i = 0; i < formInputs.length; i++) {
    const el = formInputs[i];
    if (el) el.addEventListener('keydown', onEnterKey);
  }
}
