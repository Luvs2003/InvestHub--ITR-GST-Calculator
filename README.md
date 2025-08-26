# Investor ITR & GST Calculator

A comprehensive Python-based web application for calculating capital gains tax liability from investment portfolios using the FIFO (First In, First Out) method.

## 📋 Features

- **FIFO Method**: Automatic matching of buy/sell transactions using First In, First Out principle
- **Capital Gains Classification**: 
  - STCG (Short Term Capital Gains) - Holdings ≤ 12 months
  - LTCG (Long Term Capital Gains) - Holdings > 12 months
- **GST Calculation**: Automatic 18% GST calculation on brokerage charges
- **Dividend Tracking**: Optional dividend income tracking
- **Interactive Dashboard**: User-friendly Streamlit interface
- **Export Functionality**: Download results as CSV for tax filing
- **Portfolio Insights**: Visual analysis of gains/losses by stock and type

## 🚀 Quick Start

### Local Installation

1. **Clone or download this project**
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   streamlit run app.py
   ```

4. **Open your browser** and navigate to `http://localhost:8501`

### 🌐 Deploy to Streamlit Cloud (FREE)

For detailed deployment instructions, see **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)**

**Quick steps:**
1. Create GitHub repository
2. Upload all project files
3. Connect to Streamlit Cloud
4. Deploy with one click!

**Your app will be live at**: `https://your-app-name.streamlit.app`

### Usage

1. **Prepare your CSV file** with the required format (see below)
2. **Upload the file** using the web interface
3. **Review the calculated results** including STCG, LTCG, and GST
4. **Download the analysis** for your tax filing

## 📊 CSV Format

### Required Columns

| Column | Description | Example |
|--------|-------------|---------|
| Date | Transaction date (YYYY-MM-DD) | 2023-01-15 |
| Type | Transaction type (BUY/SELL) | BUY |
| Stock | Stock/Security name | RELIANCE |
| Qty | Quantity traded | 100 |
| Price | Price per unit | 2500.00 |
| Brokerage | Brokerage charges | 25.00 |

### Optional Columns

| Column | Description | Example |
|--------|-------------|---------|
| Dividend | Dividend received | 1250.00 |

### Sample Data

```csv
Date,Type,Stock,Qty,Price,Brokerage,Dividend
2023-01-15,BUY,RELIANCE,100,2500.00,25.00,0
2023-06-20,SELL,RELIANCE,50,2650.00,15.00,0
```

## 📁 Project Structure

```
investor-tax-calculator/
├── app.py                 # Main Streamlit application
├── calculator.py          # Core calculation logic
├── requirements.txt       # Python dependencies
├── sample_portfolio.csv   # Sample data for testing
└── README.md             # This file
```

## 🧮 Calculation Method

### FIFO Matching
- Matches sell transactions with the earliest available buy transactions
- Maintains separate queues for each stock
- Handles partial quantity matches automatically

### Capital Gains Classification
- **STCG**: Holdings for 12 months or less
- **LTCG**: Holdings for more than 12 months
- Based on the difference between buy date and sell date

### GST Calculation
- Applied at 18% on all brokerage charges
- Calculated proportionally for partial matches

### Final Taxable Income
```
Final Taxable Income = Total STCG + Total LTCG + Total Dividends
```

## 📈 Output Features

### Summary Dashboard
- Total STCG and LTCG amounts
- Total dividend income
- GST on brokerage charges
- Final taxable income calculation

### Detailed Trade Analysis
- Buy/Sell date pairs
- Holding period for each trade
- Gain/Loss calculation
- STCG/LTCG classification
- GST breakdown

### Export Options
- Detailed trades CSV
- Tax summary CSV
- Formatted for ITR filing

## 🔧 Technical Details

### Dependencies
- **Streamlit**: Web application framework
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computations

### Key Classes
- `Trade`: Represents individual transactions
- `MatchedTrade`: Represents matched buy-sell pairs
- `InvestorCalculator`: Main calculation engine

## 📝 Example Usage

1. **Start the application**:
   ```bash
   streamlit run app.py
   ```

2. **Upload sample data**:
   - Use the provided `sample_portfolio.csv`
   - Or create your own following the format

3. **Review results**:
   - Check the summary metrics
   - Analyze detailed trade breakdowns
   - Download CSV reports

## ⚠️ Important Notes

- This tool is for informational purposes only
- Please consult a tax professional for official advice
- Ensure your data follows the required CSV format
- The tool assumes equity investments (12-month LTCG threshold)

## 🐛 Troubleshooting

### Common Issues

1. **File upload errors**: Check CSV format and column names
2. **Date parsing errors**: Ensure dates are in YYYY-MM-DD format
3. **Calculation errors**: Verify that sell quantities don't exceed available buy quantities

### Error Messages
- Missing required columns: Add all required CSV columns
- Insufficient buy quantity: Check that total sell quantity doesn't exceed total buy quantity for any stock
- Invalid date format: Use YYYY-MM-DD format for all dates

## 📞 Support

For issues or questions:
1. Check the troubleshooting section above
2. Verify your CSV file format
3. Ensure all dependencies are installed correctly

## 🎯 Future Enhancements

- Support for different asset classes (bonds, mutual funds)
- Multiple tax year analysis
- Advanced filtering and sorting options
- Integration with popular broker APIs
- Automated tax form generation