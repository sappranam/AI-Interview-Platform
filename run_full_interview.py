import os
import sys
import subprocess

def run_script(command):
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError:
        print(f"❌ Error running: {' '.join(command)}")
        sys.exit(1)

def main():
    if len(sys.argv) != 2:
        print("Usage: python run_full_interview.py <path_to_resume.pdf>")
        sys.exit(1)

    resume_path = sys.argv[1]

    if not os.path.exists(resume_path):
        print(f"❌ File not found: {resume_path}")
        sys.exit(1)

    print("\n🔍 Step 1: Parsing Resume...")
    run_script(["python", "parser.py", resume_path])

    print("\n🧠 Step 2: Generating Interview Questions...")
    run_script(["python", "interviewer.py"])

    print("\n🎤 Step 3: Running Interview Session...")
    run_script(["python", "interview_session.py"])

    print("\n📊 Step 4: Evaluating Answers...")
    run_script(["python", "evaluate.py"])

    print("\n✅ All done! Your evaluation report is saved as 'report.txt'.")

if __name__ == "__main__":
    main()
