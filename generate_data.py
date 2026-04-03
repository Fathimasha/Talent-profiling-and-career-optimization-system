import pandas as pd
import numpy as np
import random

# Base data pieces to procedurally generate new consultancies
REAL_NAMES = ["Tech", "Global", "City", "Urban", "Prime", "Silver", "Bright", "NextGen", "Core", "Blue", "Summit", "Talent", "HR", "Staffing", "Consulting", "Partners", "Advisory"]
FAKE_NAMES = ["Guaranteed", "Quick", "Instant", "100%", "Easy", "SureShot", "Dream", "Cash", "Pay", "First", "Job", "Placement", "Offer", "Overseas", "Visas"]

REAL_DESC_FRAGMENTS = [
    "We are an IT staffing firm partnering with MNC clients.",
    "No fees are collected from candidates at any stage.",
    "Official recruitment partner for mid-size software companies.",
    "Candidates are hired as full time employees with standard background checks.",
    "Selection process includes technical test and HR round.",
    "We are paid by employers, not by job seekers.",
    "All communication happens from verified company email domains.",
    "Provides project-based hiring for Java and .NET engineers.",
    "Consulting and training firm in data science.",
    "All openings are listed on our official website.",
    "Service charges are billed only to client companies.",
    "Works only on retained search basis.",
    "Recruitment for clients is free for job seekers."
]

FAKE_DESC_FRAGMENTS = [
    "Get selected instantly for high-paying job. Just pay registration fee.",
    "NO INTERVIEW required. Send joining fee on Google Pay.",
    "Earn daily 3000 INR. First pay processing fee for ID card.",
    "We guarantee job in MNC without exams. Pay security deposit.",
    "One-time registration fee required before sharing interview location.",
    "Company charges for profile activation. Refund if not selected.",
    "Simple work from mobile. Join now by paying account creation fee.",
    "100% placement guarantee. Freshers must pay placement fee.",
    "Part-time copy paste work. First transfer processing fee.",
    "Must pay consultancy fee and visa processing amount in advance.",
    "Pay joining fee to access premium job list and HR contacts.",
    "Activation fee must be paid immediately to unlock projects.",
    "Asks candidates to pay processing fee in cash before employer details.",
    "Demands non-refundable registration fee to reserve offer letter."
]

def generate_dataset(num_rows=900):
    rows = []
    for _ in range(num_rows):
        is_fake = random.choice([True, False])
        
        if is_fake:
            name = f"{random.choice(FAKE_NAMES)}{random.choice(FAKE_NAMES)} {random.choice(['Consultancy', 'Jobs', 'Services', 'Agency'])}"
            desc = f"{random.choice(FAKE_DESC_FRAGMENTS)} {random.choice(FAKE_DESC_FRAGMENTS)}"
            
            # 90% of fakes explicitly ask for a fee in the data column
            asks_fee = 1 if random.random() < 0.9 else 0 
            
            # To add realism/difficulty, some fakes might be subtle and NOT use obvious keywords in desc
            if random.random() < 0.1:
                desc = "We offer premium job placement services for freshers and experienced candidates."
                
            label = 1
        else:
            name = f"{random.choice(REAL_NAMES)}{random.choice(REAL_NAMES)} {random.choice(['HR', 'Staffing', 'Solutions', 'Partners'])}"
            desc = f"{random.choice(REAL_DESC_FRAGMENTS)} {random.choice(REAL_DESC_FRAGMENTS)}"
            
            # 5% of real companies might ambiguously talk about fees (e.g., training fees) but are legitimate
            asks_fee = 1 if random.random() < 0.05 else 0
            
            # To add realism/difficulty, some real ones might sound slightly sketch but are real
            if random.random() < 0.1:
                desc = "We provide 100 percent placement assistance after our intensive 6-month paid bootcamp. Recruitment itself is free."
                asks_fee = 1

            label = 0
            
        rows.append({"name": name, "description": desc, "asks_fee": asks_fee, "label": label})
        
    return pd.DataFrame(rows)

if __name__ == "__main__":
    print("Generating expanded dataset...")
    df_new = generate_dataset(900)
    
    # Load original
    df_orig = pd.read_csv("data/consultancies_dataset.csv")
    
    # Combine and shuffle
    df_combined = pd.concat([df_orig, df_new], ignore_index=True)
    df_combined = df_combined.sample(frac=1, random_state=42).reset_index(drop=True)
    
    # Save
    df_combined.to_csv("data/consultancies_dataset.csv", index=False)
    print(f"Successfully expanded dataset to {len(df_combined)} rows!")
