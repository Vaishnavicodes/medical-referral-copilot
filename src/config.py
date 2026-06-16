# Column mapping: logical key → Silver table column name.
COLUMNS = {
    "id":               "unique_id",
    "name":             "name",
    "city":             "city",
    "state":            "state",
    "postcode":         "postcode",
    "latitude":         "latitude",
    "longitude":        "longitude",
    "geo_source":       "geo_source",   # ORIGINAL/POSTCODE/CITY_AVG/STATE_AVG/UNKNOWN
    "geo_valid":        "geo_valid",    # True if any coordinate was resolved
    "specialties":      "specialties",
    "description":      "description",
    "capability":       "capability",
    "procedure":        "procedure_text",
    "equipment":        "equipment",
    "num_doctors":      "num_doctors",
    "capacity":         "capacity",
    "year_established": "year_established",
    "source_urls":      "source_urls",
    "phone":            "phone",
    "website":          "website",
    "org_type":         "organization_type",
    "completeness":     "completeness_score",
}

# Silver pre-flattens all JSON arrays — no runtime parsing needed.
ARRAY_FIELDS = []

# Fields scanned for "matching evidence"
EVIDENCE_TEXT_FIELDS = ["specialties", "description", "capability", "procedure", "equipment"]

# Fields whose absence is flagged as "missing evidence"
COMPLETENESS_FIELDS = ["num_doctors", "capacity", "year_established", "source_urls"]

# Care-need synonyms.
# Silver expands camelCase specialty codes to space-separated words:
#   emergencyMedicine  -> "emergency Medicine"  (searches as "emergency medicine")
#   orthopedicSurgery  -> "orthopedic Surgery"  (searches as "orthopedic surgery")
# Synonyms use the plain-English form so they match both expanded Silver text
# and verbose description/procedure/capability fields.
CARE_NEED_SYNONYMS = {
    "dialysis": [
        "dialysis", "hemodialysis", "haemodialysis",
        "renal care", "renal medicine",
        "nephrology", "kidney", "peritoneal",
        # layman
        "kidney failure", "kidney problem", "kidney disease",
        "my kidney", "renal", "kidney hurts",
    ],
    "emergency": [
        "emergency medicine", "emergency surgery", "emergency care",
        "emergency department", "emergency preparedness",
        "trauma", "casualty", "accident", "injury", "injured",
        "urgent care", "critical", "unconscious", "bleeding",
        "chest pain", "heart attack", "stroke",
        # layman
        "emergency", "urgent", "serious", "very serious",
        "not breathing", "stopped breathing", "passed out", "fainted",
        "heavy bleeding", "severe bleeding", "not conscious",
        "life threatening", "need help immediately", "help me",
        "road accident", "car accident", "bike accident",
    ],
    "cardiology": [
        "cardiology", "cardiac", "heart",
        "interventional cardiology", "cardiothoracic",
        "heart failure", "cath lab", "angioplasty", "bypass",
        # layman
        "chest", "chest hurts", "chest tightness", "chest pressure",
        "heart pain", "heart problem", "heart beating fast",
        "heart racing", "palpitation", "irregular heartbeat",
        "pulse", "heart condition", "my heart",
    ],
    "maternity": [
        # American spellings (camelCase expanded by Silver)
        "gynecology and obstetrics", "gynecology", "obstetrics", "obstetric",
        # British spellings — widely used in Indian hospitals
        "gynaecology and obstetrics", "gynaecology", "gynaecological", "obstetrical",
        # Common Indian abbreviations
        "obg", "ob/g", "ob-g", "ob&g",
        # Newborn / perinatal
        "neonatology", "perinatal", "nicu", "sncu", "newborn care",
        # Antenatal / postnatal (single and two-word forms)
        "maternal", "maternity",
        "antenatal", "ante natal", "prenatal", "pre natal",
        "postnatal", "post natal", "postpartum", "post partum",
        # Delivery & women's health
        "labour ward", "labor ward", "delivery room", "delivery suite",
        "birthing", "caesarean", "cesarean", "midwifery",
        "women's hospital", "women hospital", "mother and child",
        "reproductive health", "family planning",
        "fetal", "foetal",
        # layman
        "pregnant", "pregnancy", "having a baby", "about to deliver",
        "due date", "expecting", "expecting a baby", "going into labour",
        "going into labor", "water broke", "contractions",
        "just gave birth", "just delivered", "new mother",
    ],
    "oncology": [
        "oncology", "cancer",
        "medical oncology", "surgical oncology",
        "radiation oncology", "gynecological oncology",
        "chemotherapy", "radiotherapy", "tumor",
        # layman
        "tumour", "lump", "growth", "mass", "malignant",
        "cancer treatment", "chemo", "radiation treatment",
    ],
    "orthopedics": [
        "orthopedic", "orthopaedic",
        "bone", "fracture", "broken", "broken bone",
        "joint replacement", "joint reconstruction",
        "spine", "spinal",
        "knee", "hip replacement", "back pain", "dislocation", "sprain",
        "leg injury", "leg pain", "arm injury", "shoulder injury",
        "musculoskeletal", "ligament", "tendon",
        # layman — body parts
        "leg", "arm", "ankle", "wrist", "elbow", "hip", "shoulder", "joint",
        # layman — descriptions
        "hurt my leg", "hurt leg", "hurt my arm", "hurt my knee",
        "hurt my back", "hurt my shoulder", "hurt my ankle", "hurt my wrist",
        "my leg hurts", "my arm hurts", "my knee hurts", "my back hurts",
        "my shoulder hurts", "my ankle hurts", "my wrist hurts",
        "twisted my ankle", "twisted ankle", "sprained ankle", "sprained knee",
        "fell down", "i fell", "fell and hurt", "slipped and fell",
        "broken leg", "broken arm", "broken wrist", "broken ankle",
        "can't walk", "cannot walk", "difficulty walking",
        "swollen knee", "swollen ankle", "swollen joint",
        "neck pain", "neck problem", "stiff neck",
    ],
    "icu": [
        "critical care medicine", "critical care",
        "intensive care", "ventilator", "icu",
        # layman
        "very critical", "life support", "on ventilator",
    ],
    "neurology": [
        "neurology", "neurosurgery", "neuro",
        "spine neurosurgery", "peripheral nerve",
        "stroke", "brain", "epilepsy", "parkinson",
        # layman
        "head", "brain problem", "brain injury",
        "seizure", "fits", "convulsion", "body shaking",
        "paralysis", "paralysed", "paralyzed", "one side weak",
        "sudden numbness", "numbness", "numb", "tingling",
        "memory loss", "memory problem", "forgetting things",
        "dizziness", "dizzy", "balance problem", "can't balance",
        "vision loss", "sudden blindness",
        "migraine", "severe headache", "worst headache",
        "slurred speech", "speech problem", "can't speak",
    ],
    "ophthalmology": [
        "ophthalmology", "eye", "cataract", "retina",
        "glaucoma", "cornea", "vision", "optical",
        "eye pain", "eye infection", "eye injury", "blurred vision",
        "foreign body eye", "optometry", "lasik",
        # layman
        "eyes", "can't see", "cannot see", "poor vision", "weak eyesight",
        "blurry vision", "something in my eye", "something in eye",
        "eye hurts", "eye problem", "eye swollen", "red eye",
        "eye discharge", "watery eyes", "eye irritation",
    ],
    "pediatrics": [
        "pediatric", "paediatric",
        "neonatology", "neonatal", "infant",
        "child",
        # layman
        "baby", "kid", "kids", "toddler", "newborn",
        "my child", "my baby", "my kid", "my son", "my daughter",
        "child is sick", "baby is sick", "kid is sick",
        "child has fever", "baby has fever",
        "children", "minor", "young child",
    ],
    "general surgery": [
        "general surgery", "surgery",
        "laparoscopy", "hernia", "appendectomy", "gastrointestinal",
        # layman
        "appendix", "appendix pain", "appendix problem",
        "hernia problem", "needs surgery", "require surgery",
        "gallbladder", "gallstone",
    ],
    "radiology": [
        "radiology", "imaging", "mri", "ct scan", "x-ray",
        "ultrasound", "diagnostic imaging", "pet scan",
        # layman
        "scan", "need a scan", "x ray", "xray",
        "mri scan", "ct scan", "ultrasound scan",
    ],
    "ent": [
        "otolaryngology", "ent", "ear nose throat",
        "hearing", "sinusitis", "tonsil",
        # layman
        "ear", "ears", "nose", "throat",
        "ear pain", "earache", "ear hurts", "ear infection",
        "nose blocked", "blocked nose", "runny nose",
        "throat pain", "sore throat", "throat infection",
        "can't hear", "hearing loss", "ringing in ear",
        "tonsils", "tonsillitis", "snoring",
    ],
    "dermatology": [
        "dermatology", "skin", "dermatitis", "eczema", "psoriasis",
        # layman
        "rash", "itching", "itch", "itchy", "itchy skin",
        "skin problem", "skin disease", "skin infection",
        "pimples", "acne", "boil", "blister", "hives",
        "skin peeling", "dry skin", "scaly skin",
        "hair loss", "hair fall", "dandruff",
        "fungal infection", "ringworm",
    ],
    "psychiatry": [
        "psychiatry", "neuropsychiatry", "psychology", "mental health",
        "behavioral", "addiction", "rehabilitation",
        # layman
        "mental", "depression", "depressed", "feeling depressed",
        "anxiety", "anxious", "panic attack", "panic",
        "stress", "too much stress", "mental problem",
        "suicidal", "want to hurt myself",
        "mood swings", "mood problem", "behavior problem",
        "not sleeping", "insomnia", "sleep problem",
        "alcohol addiction", "drug addiction", "de-addiction",
        "feeling hopeless", "feeling worthless",
    ],
    "general medicine": [
        "general medicine", "internal medicine", "general practice",
        "family medicine", "primary care", "outpatient",
        "fever", "cold", "cough", "flu", "influenza",
        "body ache", "body pain", "headache", "fatigue",
        "vomiting", "nausea", "diarrhea", "loose motion",
        "weakness", "rash", "allergy", "infection",
        "diabetes", "hypertension", "blood pressure",
        "thyroid", "anaemia", "anemia",
        # layman
        "sick", "ill", "unwell", "not feeling well", "feeling sick",
        "not feeling good", "feeling weak", "feeling tired",
        "temperature", "high temperature", "low grade fever",
        "runny nose", "stuffy nose", "sneezing",
        "body weakness", "loss of appetite", "not eating",
        "sugar", "sugar level", "bp", "cholesterol",
        "routine checkup", "general checkup", "health checkup",
        "vaccination", "vaccine", "booster",
    ],
    "pulmonology": [
        "pulmonology", "respiratory", "lung", "pulmonary",
        "asthma", "bronchitis", "pneumonia", "copd",
        "breathing difficulty", "shortness of breath", "cough blood",
        # layman
        "breathing", "breath", "breathless", "breathlessness",
        "can't breathe", "cannot breathe", "difficulty breathing",
        "chest congestion", "wheezing", "wheeze",
        "coughing a lot", "persistent cough", "dry cough",
        "lungs", "lung problem", "lung infection",
        "oxygen level low", "oxygen dropping",
    ],
    "gastroenterology": [
        "gastroenterology", "gastro", "liver", "hepatology",
        "stomach", "abdomen", "gut", "bowel", "digestive",
        "ulcer", "jaundice", "hepatitis", "pancreatitis",
        "endoscopy", "colonoscopy",
        # layman
        "stomach pain", "stomach ache", "tummy ache", "tummy pain",
        "belly pain", "belly ache", "abdominal pain",
        "stomach hurts", "my stomach", "stomach problem",
        "acidity", "acid reflux", "heartburn", "burping",
        "constipation", "no bowel movement", "hard stool",
        "blood in stool", "black stool",
        "vomiting blood", "nausea and vomiting",
        "swollen belly", "bloated", "gas problem",
        "yellow eyes", "yellow skin", "jaundice",
    ],
    "urology": [
        "urology", "urinary", "kidney stone", "prostate",
        "bladder", "ureter", "urethra", "uti",
        "burning urination", "blood in urine",
        # layman
        "urine", "urination", "peeing", "pee",
        "burning when urinating", "burning while peeing",
        "pain while urinating", "pain while peeing",
        "blood in urine", "blood while peeing",
        "frequent urination", "urinating too much",
        "unable to urinate", "can't pee", "cannot urinate",
        "stone in kidney", "kidney stone pain",
        "prostate problem", "prostate",
    ],
}
