/**
 * LoanWise - Loan Calculator
 * Supports multiple currencies.
 */

document.addEventListener('DOMContentLoaded', () => {
  initCalculator();
});

// ============ Calculator ============
const CURRENCIES = ['USD', 'EUR', 'GBP', 'MAD', 'CAD', 'CHF', 'JPY', 'AED'];

function initCalculator() {
  const currencySelect = document.getElementById('currency');
  const loanAmountInput = document.getElementById('loanAmount');
  const interestRateInput = document.getElementById('interestRate');
  const loanTermInput = document.getElementById('loanTerm');
  const calculateBtn = document.getElementById('calculateBtn');
  const monthlyPaymentOutput = document.getElementById('monthlyPayment');
  const totalPaymentOutput = document.getElementById('totalPayment');
  const totalInterestOutput = document.getElementById('totalInterest');

  if (!currencySelect) return;

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

  function clearResults() {
    if (monthlyPaymentOutput) monthlyPaymentOutput.textContent = '—';
    if (totalPaymentOutput) totalPaymentOutput.textContent = '—';
    if (totalInterestOutput) totalInterestOutput.textContent = '—';
    [monthlyPaymentOutput, totalPaymentOutput, totalInterestOutput].forEach(el => {
      if (el) el.classList.remove('has-value');
    });
  }

  function setResults(monthly, total, interest, currency) {
    if (monthlyPaymentOutput) {
      monthlyPaymentOutput.textContent = formatCurrency(monthly, currency);
      monthlyPaymentOutput.classList.add('has-value');
    }
    if (totalPaymentOutput) {
      totalPaymentOutput.textContent = formatCurrency(total, currency);
      totalPaymentOutput.classList.add('has-value');
    }
    if (totalInterestOutput) {
      totalInterestOutput.textContent = formatCurrency(interest, currency);
      totalInterestOutput.classList.add('has-value');
    }
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

  if (calculateBtn) calculateBtn.addEventListener('click', handleCalculate);

  const formInputs = [currencySelect, loanAmountInput, interestRateInput, loanTermInput];
  formInputs.forEach((el) => {
    if (el) el.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        e.preventDefault();
        handleCalculate();
      }
    });
  });
}
