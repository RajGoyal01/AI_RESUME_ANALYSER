"""
Resume Analyser Module - Scores resumes against MNC standards and domain expectations.
"""
import re
from typing import Dict, List
from config import (DOMAIN_SKILLS, MNC_STANDARDS, SCORING_WEIGHTS, SOFT_SKILLS, ACTION_VERBS, SECTION_KEYWORDS)

def find_skills_in_text(text, skill_list):
    text_lower = text.lower()
    found = []
    for skill in skill_list:
        pattern = r'\b' + re.escape(skill.lower()) + r'\b'
        if re.search(pattern, text_lower):
            found.append(skill)
    return found

def analyze_resume(parsed_data, domain, course, branch):
    text = parsed_data.get("raw_text", "")
    text_lower = text.lower()
    sections = parsed_data.get("sections", {})
    results = {"scores": {}, "details": {}, "suggestions": [], "weak_areas": [], "strong_areas": [], "overall_score": 0}

    # Get domain skills
    domain_key = branch if branch in DOMAIN_SKILLS else domain if domain in DOMAIN_SKILLS else "Computer Science"
    skills_db = DOMAIN_SKILLS.get(domain_key, DOMAIN_SKILLS["Computer Science"])

    # 1. SKILLS MATCH ANALYSIS
    found_core = find_skills_in_text(text, skills_db.get("core", []))
    found_prog = find_skills_in_text(text, skills_db.get("programming", []))
    found_fw = find_skills_in_text(text, skills_db.get("frameworks", []))
    found_tech = find_skills_in_text(text, skills_db.get("technologies", []))
    all_found = found_core + found_prog + found_fw + found_tech
    total_possible = len(skills_db.get("core",[])) + len(skills_db.get("programming",[])) + len(skills_db.get("frameworks",[])) + len(skills_db.get("technologies",[]))
    skills_pct = (len(all_found) / max(total_possible, 1)) * 100
    skills_score = min(skills_pct * 2.5, 100)  # Scale up but cap at 100
    results["scores"]["skills_match"] = round(skills_score)
    results["details"]["skills"] = {
        "found_core": found_core, "found_programming": found_prog,
        "found_frameworks": found_fw, "found_technologies": found_tech,
        "total_found": len(all_found), "total_possible": total_possible,
        "missing_core": [s for s in skills_db.get("core",[]) if s not in found_core],
        "missing_programming": [s for s in skills_db.get("programming",[]) if s not in found_prog],
    }

    # 2. EXPERIENCE QUALITY
    exp_section = sections.get("experience", "")
    exp_score = 0
    action_verbs_found = find_skills_in_text(exp_section or text, ACTION_VERBS)
    has_metrics = bool(re.search(r'\d+%|\d+\s*(?:users|clients|projects|team|members|revenue|sales)', text_lower))
    exp_score = min(len(action_verbs_found) * 8, 50) + (25 if has_metrics else 0) + (25 if exp_section else 0)
    results["scores"]["experience_quality"] = min(round(exp_score), 100)
    results["details"]["experience"] = {"action_verbs_found": action_verbs_found, "has_metrics": has_metrics, "has_section": bool(exp_section)}

    # 3. EDUCATION SCORE
    edu = parsed_data.get("education", [])
    edu_score = 40 if edu else 0
    if "education" in sections: edu_score += 20
    gpa_found = False
    for e in edu:
        if "gpa" in e:
            gpa_found = True
            try:
                gpa = float(e["gpa"])
                if gpa <= 10: edu_score += (gpa / 10) * 40
                else: edu_score += (gpa / 100) * 40
            except: edu_score += 20
    if not gpa_found: edu_score += 20
    results["scores"]["education"] = min(round(edu_score), 100)

    # 4. PROJECTS SCORE
    proj_count = parsed_data.get("project_count", 0)
    proj_score = min(proj_count * 25, 100)
    has_proj_section = "projects" in sections
    if has_proj_section: proj_score = max(proj_score, 30)
    results["scores"]["projects"] = min(round(proj_score), 100)
    results["details"]["projects"] = {"count": proj_count, "has_section": has_proj_section}

    # 5. FORMATTING SCORE
    fmt_score = 0
    word_count = parsed_data.get("word_count", 0)
    if 200 <= word_count <= 1000: fmt_score += 30
    elif 100 <= word_count <= 1500: fmt_score += 20
    else: fmt_score += 10
    section_count = len([s for s in sections if s != "header"])
    fmt_score += min(section_count * 10, 40)
    if parsed_data.get("email"): fmt_score += 10
    if parsed_data.get("phone"): fmt_score += 10
    if parsed_data.get("name"): fmt_score += 10
    results["scores"]["formatting"] = min(round(fmt_score), 100)

    # 6. ATS KEYWORDS
    ats_keywords = skills_db.get("core", []) + skills_db.get("programming", [])[:5]
    ats_found = find_skills_in_text(text, ats_keywords)
    ats_score = min((len(ats_found) / max(len(ats_keywords), 1)) * 150, 100)
    results["scores"]["keywords_ats"] = round(ats_score)

    # 7. CERTIFICATIONS
    cert_section = sections.get("certifications", "")
    cert_score = 60 if cert_section else 0
    cert_keywords = ["certified", "certification", "certificate", "coursera", "udemy", "aws certified", "google certified", "microsoft certified", "oracle"]
    cert_found = find_skills_in_text(text, cert_keywords)
    cert_score += min(len(cert_found) * 15, 40)
    results["scores"]["certifications"] = min(round(cert_score), 100)

    # 8. ACHIEVEMENTS
    ach_section = sections.get("achievements", "")
    ach_score = 50 if ach_section else 0
    ach_keywords = ["award", "winner", "first place", "rank", "topper", "scholarship", "published", "patent", "hackathon", "competition"]
    ach_found = find_skills_in_text(text, ach_keywords)
    ach_score += min(len(ach_found) * 15, 50)
    results["scores"]["achievements"] = min(round(ach_score), 100)

    # 9. SOFT SKILLS
    ss_found = find_skills_in_text(text, SOFT_SKILLS)
    ss_score = min(len(ss_found) * 12, 100)
    results["scores"]["soft_skills"] = round(ss_score)
    results["details"]["soft_skills"] = ss_found

    # CALCULATE OVERALL SCORE
    overall = 0
    for key, weight in SCORING_WEIGHTS.items():
        overall += results["scores"].get(key, 0) * weight
    results["overall_score"] = round(overall)

    # MNC COMPARISON
    mnc_scores = {}
    for company, standards in MNC_STANDARDS.items():
        focus_found = find_skills_in_text(text, standards["focus"])
        company_score = (len(focus_found) / max(len(standards["focus"]), 1)) * 60
        if proj_count >= standards["projects_expected"]: company_score += 20
        if len(all_found) >= standards["min_skills"]: company_score += 20
        mnc_scores[company] = min(round(company_score), 100)
    results["mnc_scores"] = mnc_scores

    # WEAK AREAS & SUGGESTIONS
    missing_core = results["details"]["skills"].get("missing_core", [])
    missing_prog = results["details"]["skills"].get("missing_programming", [])

    if missing_core:
        results["weak_areas"].append({
            "area": "Core Domain Knowledge",
            "severity": "high" if len(missing_core) > len(skills_db.get("core",[])) * 0.5 else "medium",
            "missing": missing_core[:8],
            "suggestion": f"Focus on learning: {', '.join(missing_core[:5])}. These are essential for {domain_key} roles at top MNCs."
        })
    if missing_prog:
        results["weak_areas"].append({
            "area": "Programming Languages",
            "severity": "high" if len(missing_prog) > 5 else "medium",
            "missing": missing_prog[:6],
            "suggestion": f"Add proficiency in: {', '.join(missing_prog[:4])}. Practice on LeetCode/HackerRank."
        })
    if results["scores"]["experience_quality"] < 50:
        results["weak_areas"].append({
            "area": "Experience Description",
            "severity": "high",
            "missing": [],
            "suggestion": "Use strong action verbs (Built, Designed, Implemented) and quantify achievements with metrics (e.g., 'Improved performance by 40%')."
        })
    if results["scores"]["projects"] < 50:
        results["weak_areas"].append({
            "area": "Projects Portfolio",
            "severity": "high",
            "missing": [],
            "suggestion": f"Add at least 3 significant projects. MNCs like Google expect {MNC_STANDARDS['Google']['projects_expected']}+ projects. Include tech stack and impact."
        })
    if results["scores"]["certifications"] < 40:
        results["weak_areas"].append({
            "area": "Certifications",
            "severity": "low",
            "missing": [],
            "suggestion": "Add relevant certifications from Coursera, Udemy, or vendor-specific (AWS, Google, Microsoft) to boost credibility."
        })
    if not parsed_data.get("links", {}).get("github"):
        results["weak_areas"].append({
            "area": "GitHub Profile",
            "severity": "medium",
            "missing": [],
            "suggestion": "Add your GitHub profile link. Recruiters at tech companies actively review GitHub contributions."
        })
    if not parsed_data.get("links", {}).get("linkedin"):
        results["weak_areas"].append({
            "area": "LinkedIn Profile",
            "severity": "medium",
            "missing": [],
            "suggestion": "Add your LinkedIn profile link. It's essential for professional networking and recruiter discovery."
        })
    if results["scores"]["formatting"] < 60:
        results["weak_areas"].append({
            "area": "Resume Formatting",
            "severity": "medium",
            "missing": [],
            "suggestion": "Ensure your resume has clear sections: Summary, Education, Skills, Experience, Projects, Certifications. Keep it 1-2 pages."
        })

    # STRONG AREAS
    if found_core: results["strong_areas"].append(f"Core Skills: {', '.join(found_core[:5])}")
    if found_prog: results["strong_areas"].append(f"Programming: {', '.join(found_prog[:5])}")
    if found_fw: results["strong_areas"].append(f"Frameworks: {', '.join(found_fw[:5])}")
    if action_verbs_found: results["strong_areas"].append(f"Good use of action verbs: {', '.join(action_verbs_found[:3])}")
    if has_metrics: results["strong_areas"].append("Quantified achievements with metrics")

    # OVERALL SUGGESTIONS
    if results["overall_score"] >= 80:
        results["suggestions"].append("Excellent resume! Fine-tune with company-specific keywords for each application.")
    elif results["overall_score"] >= 60:
        results["suggestions"].append("Good foundation. Focus on the weak areas identified to reach MNC standards.")
    elif results["overall_score"] >= 40:
        results["suggestions"].append("Your resume needs significant improvement. Prioritize adding projects, skills, and quantified experience.")
    else:
        results["suggestions"].append("Major overhaul recommended. Build projects, learn core skills, and restructure your resume with proper formatting.")

    results["grade"] = "A+" if results["overall_score"] >= 90 else "A" if results["overall_score"] >= 80 else "B+" if results["overall_score"] >= 70 else "B" if results["overall_score"] >= 60 else "C+" if results["overall_score"] >= 50 else "C" if results["overall_score"] >= 40 else "D" if results["overall_score"] >= 30 else "F"

    # ─── COMPANY SELECTION CHANCES ───
    company_recommendations = []
    for company, standards in MNC_STANDARDS.items():
        company_domains = standards.get("domains", [])
        tier = standards.get("tier", 3)
        min_score = standards.get("min_score", 50)
        hiring_bar = standards.get("hiring_bar", "Medium")
        emoji = standards.get("emoji", "🔹")

        # Check domain match
        domain_match = domain_key in company_domains
        focus_found = find_skills_in_text(text, standards["focus"])
        focus_pct = (len(focus_found) / max(len(standards["focus"]), 1)) * 100

        # Calculate selection chance
        chance_score = 0
        # Overall resume quality (40%)
        chance_score += min(results["overall_score"] / 100, 1) * 40
        # Focus skill alignment (30%)
        chance_score += (focus_pct / 100) * 30
        # Domain relevance (15%)
        if domain_match:
            chance_score += 15
        else:
            chance_score += 3
        # Projects & experience bonus (15%)
        proj_bonus = min(proj_count / max(standards["projects_expected"], 1), 1) * 8
        skill_bonus = min(len(all_found) / max(standards["min_skills"], 1), 1) * 7
        chance_score += proj_bonus + skill_bonus

        chance_score = round(min(chance_score, 100))

        # Determine selection level
        if chance_score >= 75:
            level = "High"
            level_color = "success"
            tip = f"Strong match! Focus on {company}-specific interview prep."
        elif chance_score >= 55:
            level = "Good"
            level_color = "primary"
            tip = f"Good chances. Improve: {', '.join([s for s in standards['focus'] if s.lower() not in text_lower][:3]) or 'interview skills'}."
        elif chance_score >= 35:
            level = "Moderate"
            level_color = "warning"
            missing_focus = [s for s in standards['focus'] if s.lower() not in text_lower]
            tip = f"Build skills in: {', '.join(missing_focus[:3])}." if missing_focus else "Add more projects and experience."
        else:
            level = "Low"
            level_color = "danger"
            tip = f"Significant skill gaps. Focus on: {', '.join(standards['focus'][:3])}."

        company_recommendations.append({
            "company": company,
            "emoji": emoji,
            "chance_score": chance_score,
            "level": level,
            "level_color": level_color,
            "tier": tier,
            "hiring_bar": hiring_bar,
            "domain_match": domain_match,
            "focus_matched": focus_found,
            "focus_total": standards["focus"],
            "tip": tip,
        })

    # Sort: domain matches first, then by chance score
    company_recommendations.sort(key=lambda x: (-x["domain_match"], -x["chance_score"]))
    results["company_recommendations"] = company_recommendations

    return results
