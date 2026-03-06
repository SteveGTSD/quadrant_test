# 🚀 Build Quadrant.exe Using GitHub Actions (Free, No Installation Required)

This guide walks you through building the Windows executable using GitHub's free cloud service. **You don't need to install Python or any development tools on your computer.**

---

## 📋 What You'll Need

- ✅ A web browser (Chrome, Firefox, Edge, Safari)
- ✅ An email address (to create a GitHub account)
- ✅ The project files (included in this package)
- ⏱️ About 15-20 minutes

---

## Step 1: Create a Free GitHub Account

> **Skip this step if you already have a GitHub account**

1. Open your web browser and go to: **https://github.com**

2. Click the **"Sign up"** button in the top-right corner

3. Enter your information:
   - Email address
   - Create a password
   - Choose a username
   - Verify you're human (solve the puzzle)
   
4. Click **"Create account"**

5. Check your email for a verification code and enter it

6. Choose the **"Free"** plan (it's all you need!)

7. You can skip the personalization questions

✅ **You now have a GitHub account!**

---

## Step 2: Create a New Repository

A "repository" is like a folder that stores your project files.

1. After logging in, click the **"+"** button in the top-right corner
   
2. Select **"New repository"**

3. Fill in the details:
   - **Repository name**: `quadrant-chart` (or any name you prefer)
   - **Description**: `Project Quadrant Chart Generator` (optional)
   - **Visibility**: Choose **"Private"** (recommended) or "Public"
   - ✅ Check **"Add a README file"**

4. Click **"Create repository"**

✅ **Your repository is created!**

---

## Step 3: Upload the Project Files

Now we'll upload all the necessary files to your repository.

### Method A: Drag and Drop (Easiest)

1. In your repository, click **"Add file"** → **"Upload files"**

2. Open your file explorer and navigate to where you saved the project files

3. Select and drag these files/folders into the browser:
   - `quadrant.py`
   - `quadrant_config.json`
   - `requirements.txt`
   - `.github` folder (this contains the workflow)

   > **Important**: Make sure to include the `.github` folder! If you can't see it:
   > - **Mac**: Press `Cmd + Shift + .` to show hidden files
   > - **Windows**: In File Explorer, click "View" → check "Hidden items"

4. Scroll down and click **"Commit changes"**

✅ **Your files are uploaded!**

### Method B: Create Files Manually

If drag-and-drop doesn't work for you:

1. In your repository, click **"Add file"** → **"Create new file"**

2. Name it: `.github/workflows/build-windows-exe.yml`
   
   > Typing the `/` will automatically create folders

3. Copy and paste the workflow content (from the file in this package)

4. Click **"Commit new file"**

5. Repeat for the other files:
   - `quadrant.py`
   - `quadrant_config.json`
   - `requirements.txt`

---

## Step 4: Trigger the Build

Now let's build your Windows executable!

1. In your repository, click the **"Actions"** tab at the top

2. You should see **"Build Windows Executable"** in the list

3. Click on **"Build Windows Executable"**

4. Click the **"Run workflow"** button (dropdown on the right)

5. Click the green **"Run workflow"** button

6. **Wait for the build** (usually takes 2-5 minutes)
   - 🟡 Yellow dot = Building
   - ✅ Green checkmark = Success!
   - ❌ Red X = Error (see troubleshooting below)

✅ **The build is running!**

---

## Step 5: Download Your Executable

Once the build succeeds (green checkmark):

1. Click on the completed workflow run (the one with the green checkmark)

2. Scroll down to the **"Artifacts"** section

3. Click on **"Quadrant-Windows-Executable"** to download

4. The download is a ZIP file containing:
   - `Quadrant.exe` - The Windows application
   - `quadrant_config.json` - Configuration file

5. **Extract the ZIP file** to get your files

✅ **You have your Windows executable!**

---

## 🎉 How to Use Quadrant.exe

1. **Copy these files** to the same folder:
   - `Quadrant.exe`
   - `quadrant_config.json`
   - Your Excel file (e.g., `TDB_Roadmap_sc test quadrant.xlsx`)

2. **Double-click** `Quadrant.exe`

3. **View results**:
   - `quadrant.html` opens automatically in your browser
   - `quadrant_output.csv` contains detailed data

---

## 🔄 Updating Your Configuration

To customize the chart:

1. Edit `quadrant_config.json` with any text editor
2. Keep it in the same folder as `Quadrant.exe`
3. Re-run `Quadrant.exe`

You don't need to rebuild the .exe to change the configuration!

---

## 🔄 Rebuilding After Code Changes

If you modify `quadrant.py` and need to rebuild:

1. Go to your GitHub repository

2. Upload the updated `quadrant.py` file:
   - Click **"Add file"** → **"Upload files"**
   - Drag your updated file
   - Click **"Commit changes"**

3. Go to **"Actions"** tab

4. The build will start automatically (or click "Run workflow" manually)

5. Download the new `Quadrant.exe` when complete

---

## ❓ Troubleshooting

### "I don't see the Actions tab"
- Make sure you uploaded the `.github/workflows/build-windows-exe.yml` file
- The folder structure must be exactly: `.github/workflows/build-windows-exe.yml`

### "The workflow is grayed out or disabled"
- Click on the workflow name
- Click **"Enable workflow"** if shown

### "Build failed with red X"
- Click on the failed run to see the error log
- Most common issues:
  - Missing `requirements.txt` file
  - Syntax error in `quadrant.py`
  - Missing `.github/workflows` folder structure

### "I can't see the .github folder"
- Hidden files are invisible by default
- **Mac**: Press `Cmd + Shift + .`
- **Windows**: File Explorer → View → Show → Hidden items

### "Quadrant.exe won't run / Windows blocks it"
- Windows SmartScreen may block unknown apps
- Click **"More info"** → **"Run anyway"**
- Or right-click the .exe → Properties → Unblock → Apply

### "Excel file not found"
- Make sure your Excel file is in the same folder as `Quadrant.exe`
- The file must be `.xlsx` format

---

## 💡 Tips

- **Keep artifacts for 90 days**: GitHub stores your built files for 90 days by default
- **Re-download anytime**: You can re-download from the Actions tab as long as the artifact hasn't expired
- **Free limits**: GitHub Actions gives you 2,000 minutes/month free - building this takes ~3 minutes
- **Private vs Public**: Private repos use your free minutes; public repos have unlimited minutes

---

## 🆘 Need More Help?

- **GitHub Docs**: https://docs.github.com
- **GitHub Actions Guide**: https://docs.github.com/en/actions

---

*This guide was created for non-technical users. No programming experience required!*
