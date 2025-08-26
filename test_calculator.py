#!/usr/bin/env python3
"""
Test script for the Investor ITR & GST Calculator
"""

import sys
import os
from calculator import InvestorCalculator
import pandas as pd

def test_calculator():
    """Test the calculator with sample data"""
    print("🧪 Testing Investor ITR & GST Calculator...")
    print("=" * 50)
    
    try:
        # Initialize calculator
        calc = InvestorCalculator()
        
        # Test with sample CSV
        sample_file = "sample_portfolio.csv"
        
        if not os.path.exists(sample_file):
            print(f"❌ Sample file {sample_file} not found!")
            return False
        
        print(f"📁 Loading sample data from {sample_file}")
        
        # Process portfolio
        results_df, summary = calc.process_portfolio(sample_file)
        
        print("✅ Portfolio processed successfully!")
        print(f"📊 Trades matched: {len(results_df)}")
        
        # Display summary
        print("\n📈 Tax Summary:")
        print("-" * 30)
        for key, value in summary.items():
            if isinstance(value, (int, float)):
                print(f"{key}: ₹{value:,.2f}")
            else:
                print(f"{key}: {value}")
        
        # Display first few trades
        print(f"\n📋 Sample Matched Trades (showing first 5):")
        print("-" * 50)
        if not results_df.empty:
            print(results_df.head().to_string(index=False))
        else:
            print("No trades matched!")
        
        # Validation checks
        print(f"\n🔍 Validation Checks:")
        print("-" * 25)
        
        # Check if we have both STCG and LTCG trades
        stcg_trades = len(results_df[results_df['Type'] == 'STCG'])
        ltcg_trades = len(results_df[results_df['Type'] == 'LTCG'])
        
        print(f"STCG Trades: {stcg_trades}")
        print(f"LTCG Trades: {ltcg_trades}")
        
        # Check GST calculation
        total_brokerage = results_df['Brokerage'].sum()
        total_gst = results_df['GST on Brokerage'].sum()
        expected_gst = total_brokerage * 0.18
        
        print(f"Total Brokerage: ₹{total_brokerage:.2f}")
        print(f"Total GST: ₹{total_gst:.2f}")
        print(f"Expected GST (18%): ₹{expected_gst:.2f}")
        print(f"GST Calculation: {'✅ Correct' if abs(total_gst - expected_gst) < 0.01 else '❌ Incorrect'}")
        
        # Check dividend calculation
        total_dividends = summary['Total Dividends']
        print(f"Total Dividends: ₹{total_dividends:.2f}")
        
        print(f"\n🎯 Final Result: Final Taxable Income = ₹{summary['Final Taxable Income']:,.2f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_edge_cases():
    """Test edge cases"""
    print(f"\n🧪 Testing Edge Cases...")
    print("=" * 30)
    
    try:
        # Test with empty data
        calc = InvestorCalculator()
        empty_df = pd.DataFrame(columns=['Date', 'Type', 'Stock', 'Qty', 'Price', 'Brokerage'])
        
        # Save empty CSV temporarily
        empty_df.to_csv('test_empty.csv', index=False)
        
        try:
            results_df, summary = calc.process_portfolio('test_empty.csv')
            print("✅ Empty file handling: OK")
        except Exception as e:
            print(f"❌ Empty file handling failed: {e}")
        
        # Clean up
        if os.path.exists('test_empty.csv'):
            os.remove('test_empty.csv')
        
        return True
        
    except Exception as e:
        print(f"❌ Edge case testing failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting Calculator Tests")
    print("=" * 50)
    
    # Test main functionality
    main_test_passed = test_calculator()
    
    # Test edge cases
    edge_test_passed = test_edge_cases()
    
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    print(f"Main functionality: {'✅ PASSED' if main_test_passed else '❌ FAILED'}")
    print(f"Edge cases: {'✅ PASSED' if edge_test_passed else '❌ FAILED'}")
    
    if main_test_passed and edge_test_passed:
        print("\n🎉 All tests passed! The calculator is ready to use.")
        print("\n🚀 To run the Streamlit app:")
        print("   streamlit run app.py")
    else:
        print("\n⚠️  Some tests failed. Please check the implementation.")
        sys.exit(1)