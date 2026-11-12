# YottaFlex Dashboard - Render Deployment Guide

## 📋 Prerequisites

1. **GitHub Account** - Repository pushed to GitHub
2. **Render Account** - Free tier available at render.com
3. **Project Ready** - All files committed and pushed

---

## 🚀 Step-by-Step Deployment to Render

### **Step 1: Create Render Account**
- Go to https://render.com
- Sign up with GitHub account
- Authorize GitHub access

### **Step 2: Create New Web Service**
1. Click "New +" → "Web Service"
2. Connect GitHub repository
3. Select your YottaFlex repository
4. Click "Connect"

### **Step 3: Configure Service**
Fill in these details:

| Field | Value |
|-------|-------|
| **Name** | yottaflex-dashboard |
| **Environment** | Python 3 |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `streamlit run design_option_2_workbench.py --server.port=8501 --server.address=0.0.0.0` |
| **Instance Type** | Free |

### **Step 4: Set Environment Variables (Optional)**
```
STREAMLIT_SERVER_HEADLESS=true
STREAMLIT_SERVER_PORT=8501
```

### **Step 5: Deploy**
- Click "Create Web Service"
- Render will:
  - Install dependencies from `requirements.txt`
  - Run `design_option_2_workbench.py`
  - Provide public URL

### **Step 6: Access Dashboard**
Your dashboard will be live at:
```
https://yottaflex-dashboard.onrender.com
```

---

## 📁 File Structure for Deployment

```
yottaflex-loan-risk-platform/
├── design_option_2_workbench.py    ← MAIN DASHBOARD
├── generator.py
├── validate.py
├── requirements.txt                 ← Dependencies
├── .streamlit/config.toml           ← Streamlit config
├── data/                            ← CSV files (auto-generated)
│   ├── loan_applications.csv
│   ├── decisions.csv
│   ├── affordability_checks.csv
│   └── ... (10 more CSVs)
└── README.md                        ← Documentation
```

---

## ✅ Verification Checklist

Before deploying, verify:

```
☐ Python 3.8+ installed
☐ All files committed to Git
☐ Pushed to GitHub
☐ requirements.txt exists
☐ .streamlit/config.toml exists
☐ Data files in data/ directory
☐ design_option_2_workbench.py tested locally
```

**Test locally first:**
```bash
streamlit run design_option_2_workbench.py
```

Should open at: http://localhost:8501

---

## 🔧 Troubleshooting

### **Deployment Fails**
- Check build logs in Render dashboard
- Ensure `requirements.txt` lists all dependencies
- Verify Python version compatibility

### **Dashboard Won't Load**
- Check "Logs" tab in Render
- Verify data files are present
- Ensure correct working directory

### **Data Not Loading**
- Data files must be in `data/` folder
- Run `python generator.py` to create CSVs
- Verify file paths in code are relative

---

## 💰 Render Pricing

- **Free Tier**: Free (with limitations)
  - 750 hours/month
  - Shared CPU
  - 0.5GB RAM
  - Spins down after 15 min of inactivity

- **Paid Tier**: $7+/month
  - Always-on
  - Dedicated resources
  - Better performance

---

## 🔗 Dashboard Links

Once deployed:

- **Production URL**: `https://yottaflex-dashboard.onrender.com`
- **GitHub Repo**: `https://github.com/[YOUR_USERNAME]/yottaflex-loan-risk-platform`

---

## 📚 Documentation

All documentation included:
- `README.md` - Quick start
- `DATA_DICTIONARY.md` - Field definitions
- `PROJECT_BLUEPRINT.md` - Complete architecture
- `SUBMISSION_CHECKLIST.md` - YottaFlex requirements

---

**Dashboard Status**: ✅ Ready for Production Deployment

**Features**:
- 🔍 Search applications
- 📋 Application details
- 📊 Portfolio overview
- ⚙️ Decision engine
- 💾 Connected to real data
- 🎨 Professional banking styling

---

For help: https://render.com/docs
