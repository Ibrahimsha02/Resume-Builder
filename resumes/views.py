from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import HttpResponse
from .models import Resume, PersonalInfo, Education, Experience, Skill, Project, Certification, Achievement, Language
from .forms import (
    ResumeForm, PersonalInfoForm,
    EducationFormSet, ExperienceFormSet,
    SkillFormSet, ProjectFormSet, CertificationFormSet,
    AchievementFormSet, LanguageFormSet
)


def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'resumes/home.html')


@login_required
def dashboard(request):
    resumes = Resume.objects.filter(user=request.user)
    return render(request, 'resumes/dashboard.html', {'resumes': resumes})


@login_required
def create_resume(request):
    if request.method == 'POST':
        resume_form = ResumeForm(request.POST)
        personal_form = PersonalInfoForm(request.POST)

        if resume_form.is_valid() and personal_form.is_valid():
            resume = resume_form.save(commit=False)
            resume.user = request.user
            resume.save()

            personal_info = personal_form.save(commit=False)
            personal_info.resume = resume
            personal_info.save()

            education_formset = EducationFormSet(request.POST, instance=resume)
            experience_formset = ExperienceFormSet(request.POST, instance=resume)
            skill_formset = SkillFormSet(request.POST, instance=resume)
            project_formset = ProjectFormSet(request.POST, instance=resume)
            certification_formset = CertificationFormSet(request.POST, instance=resume)
            achievement_formset = AchievementFormSet(request.POST, instance=resume)
            language_formset = LanguageFormSet(request.POST, instance=resume)

            if (education_formset.is_valid() and experience_formset.is_valid() and
                skill_formset.is_valid() and project_formset.is_valid() and
                certification_formset.is_valid() and achievement_formset.is_valid() and
                language_formset.is_valid()):
                education_formset.save()
                experience_formset.save()
                skill_formset.save()
                project_formset.save()
                certification_formset.save()
                achievement_formset.save()
                language_formset.save()
                return redirect('dashboard')
    else:
        resume_form = ResumeForm()
        personal_form = PersonalInfoForm()
        education_formset = EducationFormSet()
        experience_formset = ExperienceFormSet()
        skill_formset = SkillFormSet()
        project_formset = ProjectFormSet()
        certification_formset = CertificationFormSet()
        achievement_formset = AchievementFormSet()
        language_formset = LanguageFormSet()

    context = {
        'resume_form': resume_form,
        'personal_form': personal_form,
        'education_formset': education_formset,
        'experience_formset': experience_formset,
        'skill_formset': skill_formset,
        'project_formset': project_formset,
        'certification_formset': certification_formset,
        'achievement_formset': achievement_formset,
        'language_formset': language_formset,
    }
    return render(request, 'resumes/create_resume.html', context)


@login_required
def resume_detail(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    return render(request, 'resumes/resume_detail.html', {'resume': resume})


@login_required
def resume_pdf(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    template_map = {
        'classic': 'resumes/pdf_classic.html',
        'modern': 'resumes/pdf_modern.html',
        'minimal': 'resumes/pdf_minimal.html',
    }
    template_name = template_map.get(resume.template, 'resumes/pdf_classic.html')
    template = get_template(template_name)
    html = template.render({'resume': resume})

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{resume.title}.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('PDF generation error')
    return response


@login_required
def edit_resume(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    personal_info, created = PersonalInfo.objects.get_or_create(resume=resume)

    if request.method == 'POST':
        resume_form = ResumeForm(request.POST, instance=resume)
        personal_form = PersonalInfoForm(request.POST, instance=personal_info)

        education_formset = EducationFormSet(request.POST, instance=resume)
        experience_formset = ExperienceFormSet(request.POST, instance=resume)
        skill_formset = SkillFormSet(request.POST, instance=resume)
        project_formset = ProjectFormSet(request.POST, instance=resume)
        certification_formset = CertificationFormSet(request.POST, instance=resume)
        achievement_formset = AchievementFormSet(request.POST, instance=resume)
        language_formset = LanguageFormSet(request.POST, instance=resume)

        if (resume_form.is_valid() and personal_form.is_valid() and
            education_formset.is_valid() and experience_formset.is_valid() and
            skill_formset.is_valid() and project_formset.is_valid() and
            certification_formset.is_valid() and achievement_formset.is_valid() and
            language_formset.is_valid()):

            resume_form.save()
            personal_form.save()
            education_formset.save()
            experience_formset.save()
            skill_formset.save()
            project_formset.save()
            certification_formset.save()
            achievement_formset.save()
            language_formset.save()
            return redirect('resume_detail', resume_id=resume.id)
    else:
        resume_form = ResumeForm(instance=resume)
        personal_form = PersonalInfoForm(instance=personal_info)
        education_formset = EducationFormSet(instance=resume)
        experience_formset = ExperienceFormSet(instance=resume)
        skill_formset = SkillFormSet(instance=resume)
        project_formset = ProjectFormSet(instance=resume)
        certification_formset = CertificationFormSet(instance=resume)
        achievement_formset = AchievementFormSet(instance=resume)
        language_formset = LanguageFormSet(instance=resume)

    context = {
        'resume_form': resume_form,
        'personal_form': personal_form,
        'education_formset': education_formset,
        'experience_formset': experience_formset,
        'skill_formset': skill_formset,
        'project_formset': project_formset,
        'certification_formset': certification_formset,
        'achievement_formset': achievement_formset,
        'language_formset': language_formset,
    }
    return render(request, 'resumes/create_resume.html', context)


@login_required
def delete_resume(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    if request.method == 'POST':
        resume.delete()
        return redirect('dashboard')
    return render(request, 'resumes/delete_confirm.html', {'resume': resume})


@login_required
def start_resume_with_template(request, template_name):
    valid_templates = ['classic', 'modern', 'minimal']
    if template_name not in valid_templates:
        template_name = 'classic'

    resume = Resume.objects.create(
        user=request.user,
        title="My Resume",
        template=template_name
    )
    return redirect('edit_resume', resume_id=resume.id)


SAMPLE_RESUMES = {
    'classic-1': {
        'template': 'classic', 'label': 'Classic — Software Engineer',
        'title': 'Software Engineer Resume',
        'name': 'Alex Kumar', 'email': 'alex.kumar@email.com', 'phone': '+91 98765 43210',
        'location': 'Bengaluru, India', 'linkedin': 'https://linkedin.com/in/alexkumar', 'github': 'https://github.com/alexkumar',
        'summary': 'Full stack developer with a passion for building clean, scalable web applications. Experienced in Python, Django, and JavaScript.',
        'education': [('B.Tech in Computer Science', 'ABC Institute of Technology', '2021-2025', '8.4 CGPA')],
        'experience': [('Tech Solutions Pvt Ltd', 'Software Developer Intern', 'Jan 2025 - Jun 2025', 'Built and maintained REST APIs using Django REST Framework. Collaborated with a team of 5 to ship features.')],
        'skills': ['Python', 'Django', 'JavaScript', 'HTML/CSS', 'Git', 'SQL'],
        'projects': [('Task Management App', 'A full-stack task tracker with authentication and real-time updates.', 'Django, PostgreSQL, JavaScript', 'https://github.com/alexkumar/task-manager')],
        'certifications': [('Python for Everybody', 'Coursera', '2024')],
        'achievements': ['Winner, Inter-college Hackathon 2024', 'Published article on REST API design'],
        'languages': [('English', 'Fluent'), ('Hindi', 'Native')],
    },
    'classic-2': {
        'template': 'classic', 'label': 'Classic — Marketing Executive',
        'title': 'Marketing Executive Resume',
        'name': 'Priya Sharma', 'email': 'priya.sharma@email.com', 'phone': '+91 91234 56780',
        'location': 'Mumbai, India', 'linkedin': 'https://linkedin.com/in/priyasharma', 'github': '',
        'summary': 'Results-driven marketing executive with 3+ years of experience in digital campaigns, brand strategy, and social media growth.',
        'education': [('BBA in Marketing', 'Mumbai University', '2018-2021', '75%')],
        'experience': [('BrightAds Media', 'Marketing Executive', 'Jul 2021 - Present', 'Managed digital campaigns across Meta and Google Ads, increasing lead generation by 40%.')],
        'skills': ['SEO', 'Google Ads', 'Content Strategy', 'Canva', 'Analytics', 'Email Marketing'],
        'projects': [('Brand Relaunch Campaign', 'Led rebranding campaign resulting in 25% increase in engagement.', 'Meta Ads, Google Analytics', '')],
        'certifications': [('Google Digital Marketing Certificate', 'Google', '2022')],
        'achievements': ['Employee of the Quarter, Q3 2023', 'Grew Instagram following from 2K to 20K'],
        'languages': [('English', 'Fluent'), ('Marathi', 'Native')],
    },
    'classic-3': {
        'template': 'classic', 'label': 'Classic — Mechanical Engineer',
        'title': 'Mechanical Engineer Resume',
        'name': 'Rahul Verma', 'email': 'rahul.verma@email.com', 'phone': '+91 99887 76655',
        'location': 'Pune, India', 'linkedin': 'https://linkedin.com/in/rahulverma', 'github': '',
        'summary': 'Detail-oriented mechanical engineer with experience in CAD design, product testing, and manufacturing process improvement.',
        'education': [('B.E. in Mechanical Engineering', 'Pune Institute of Engineering', '2019-2023', '8.0 CGPA')],
        'experience': [('AutoParts Ltd', 'Design Engineer', 'Aug 2023 - Present', 'Designed and tested automotive components using SolidWorks, reducing production defects by 15%.')],
        'skills': ['SolidWorks', 'AutoCAD', 'GD&T', 'Six Sigma', 'MATLAB'],
        'projects': [('Fuel Efficiency Optimizer', 'Designed a prototype to improve small engine fuel efficiency by 12%.', 'SolidWorks, ANSYS', '')],
        'certifications': [('Certified SolidWorks Associate', 'Dassault Systemes', '2023')],
        'achievements': ['Best Final Year Project Award 2023'],
        'languages': [('English', 'Fluent'), ('Hindi', 'Native')],
    },
    'modern-1': {
        'template': 'modern', 'label': 'Modern — UI/UX Designer',
        'title': 'UI/UX Designer Resume',
        'name': 'Sneha Iyer', 'email': 'sneha.iyer@email.com', 'phone': '+91 90909 12345',
        'location': 'Chennai, India', 'linkedin': 'https://linkedin.com/in/snehaiyer', 'github': 'https://github.com/snehaiyer',
        'summary': 'Creative UI/UX designer focused on crafting intuitive, user-centered digital experiences for web and mobile products.',
        'education': [('B.Des in Interaction Design', 'National Institute of Design', '2020-2024', '8.7 CGPA')],
        'experience': [('PixelCraft Studio', 'UI/UX Designer', 'Jun 2024 - Present', 'Designed end-to-end user flows and interactive prototypes for 5+ client products using Figma.')],
        'skills': ['Figma', 'Adobe XD', 'Prototyping', 'User Research', 'Wireframing'],
        'projects': [('Fitness App Redesign', 'Redesigned onboarding flow, improving completion rate by 30%.', 'Figma, Maze', 'https://github.com/snehaiyer/fitness-redesign')],
        'certifications': [('Google UX Design Certificate', 'Google', '2023')],
        'achievements': ['Featured on Behance Staff Picks 2024'],
        'languages': [('English', 'Fluent'), ('Tamil', 'Native')],
    },
    'modern-2': {
        'template': 'modern', 'label': 'Modern — Data Analyst',
        'title': 'Data Analyst Resume',
        'name': 'Karan Mehta', 'email': 'karan.mehta@email.com', 'phone': '+91 98123 45670',
        'location': 'Hyderabad, India', 'linkedin': 'https://linkedin.com/in/karanmehta', 'github': 'https://github.com/karanmehta',
        'summary': 'Data analyst skilled in transforming raw data into actionable business insights using SQL, Python, and Power BI.',
        'education': [('B.Sc in Statistics', 'Osmania University', '2020-2023', '82%')],
        'experience': [('InsightWorks Analytics', 'Data Analyst', 'Sep 2023 - Present', 'Built dashboards used by leadership, cutting reporting time by 60%.')],
        'skills': ['SQL', 'Python', 'Power BI', 'Excel', 'Pandas', 'Statistics'],
        'projects': [('Sales Forecasting Model', 'Built a regression model predicting quarterly sales with 92% accuracy.', 'Python, scikit-learn', 'https://github.com/karanmehta/sales-forecast')],
        'certifications': [('Microsoft Power BI Data Analyst', 'Microsoft', '2024')],
        'achievements': ['Reduced reporting turnaround by 60%'],
        'languages': [('English', 'Fluent'), ('Telugu', 'Native')],
    },
    'modern-3': {
        'template': 'modern', 'label': 'Modern — Product Manager',
        'title': 'Product Manager Resume',
        'name': 'Ananya Rao', 'email': 'ananya.rao@email.com', 'phone': '+91 97654 32109',
        'location': 'Bengaluru, India', 'linkedin': 'https://linkedin.com/in/ananyarao', 'github': '',
        'summary': 'Product manager with a track record of shipping user-focused features by aligning engineering, design, and business goals.',
        'education': [('MBA', 'Indian Institute of Management', '2019-2021', '3.8 GPA')],
        'experience': [('FinNext', 'Associate Product Manager', 'Jul 2021 - Present', 'Led launch of a payments feature adopted by 200K+ users within 3 months.')],
        'skills': ['Roadmapping', 'Agile', 'SQL', 'Figma', 'A/B Testing'],
        'projects': [('Payments Revamp', 'Drove end-to-end redesign of checkout flow, increasing conversion by 18%.', 'Jira, Figma', '')],
        'certifications': [('Certified Scrum Product Owner', 'Scrum Alliance', '2022')],
        'achievements': ['Launched feature used by 200K+ users'],
        'languages': [('English', 'Fluent'), ('Kannada', 'Native')],
    },
    'modern-4': {
        'template': 'modern', 'label': 'Modern — Backend Developer',
        'title': 'Backend Developer Resume',
        'name': 'Vikram Singh', 'email': 'vikram.singh@email.com', 'phone': '+91 99001 22334',
        'location': 'Gurugram, India', 'linkedin': 'https://linkedin.com/in/vikramsingh', 'github': 'https://github.com/vikramsingh',
        'summary': 'Backend developer specializing in building scalable APIs and microservices using Python and Node.js.',
        'education': [('B.Tech in Information Technology', 'Delhi Technological University', '2020-2024', '8.6 CGPA')],
        'experience': [('CloudNova Systems', 'Backend Developer', 'Jul 2024 - Present', 'Built microservices handling 1M+ daily requests using Django and Redis.')],
        'skills': ['Python', 'Django', 'Node.js', 'PostgreSQL', 'Docker', 'AWS'],
        'projects': [('Order Processing Microservice', 'Built a scalable order service handling 1M+ daily requests.', 'Django, Redis, Docker', 'https://github.com/vikramsingh/order-service')],
        'certifications': [('AWS Certified Developer Associate', 'Amazon', '2024')],
        'achievements': ['Optimized API response time by 45%'],
        'languages': [('English', 'Fluent'), ('Hindi', 'Native')],
    },
    'minimal-1': {
        'template': 'minimal', 'label': 'Minimal — Content Writer',
        'title': 'Content Writer Resume',
        'name': 'Divya Nair', 'email': 'divya.nair@email.com', 'phone': '+91 90000 11223',
        'location': 'Kochi, India', 'linkedin': 'https://linkedin.com/in/divyanair', 'github': '',
        'summary': 'Content writer with a knack for turning complex ideas into clear, engaging copy across blogs, web, and social media.',
        'education': [('B.A. in English Literature', 'University of Kerala', '2019-2022', '78%')],
        'experience': [('WordCraft Media', 'Content Writer', 'Jan 2023 - Present', 'Wrote 100+ articles and web copy pieces, growing organic traffic by 35%.')],
        'skills': ['SEO Writing', 'Copywriting', 'WordPress', 'Research', 'Editing'],
        'projects': [('Blog Growth Initiative', 'Grew a client blog from 5K to 50K monthly visitors through content strategy.', 'SEMrush, WordPress', '')],
        'certifications': [('HubSpot Content Marketing Certificate', 'HubSpot', '2023')],
        'achievements': ['Grew blog traffic 10x in one year'],
        'languages': [('English', 'Fluent'), ('Malayalam', 'Native')],
    },
    'minimal-2': {
        'template': 'minimal', 'label': 'Minimal — HR Executive',
        'title': 'HR Executive Resume',
        'name': 'Neha Gupta', 'email': 'neha.gupta@email.com', 'phone': '+91 98111 22334',
        'location': 'Noida, India', 'linkedin': 'https://linkedin.com/in/nehagupta', 'github': '',
        'summary': 'HR executive with experience in talent acquisition, employee engagement, and HR operations for fast-growing teams.',
        'education': [('MBA in Human Resources', 'Amity University', '2020-2022', '8.1 CGPA')],
        'experience': [('NexGen Corp', 'HR Executive', 'Jul 2022 - Present', 'Managed end-to-end recruitment cycle, reducing average hiring time by 20%.')],
        'skills': ['Recruitment', 'Onboarding', 'HRMS', 'Employee Relations', 'Excel'],
        'projects': [('Employee Engagement Program', 'Designed a quarterly engagement program improving retention by 15%.', 'Survey tools, HRMS', '')],
        'certifications': [('SHRM Certified Professional', 'SHRM', '2023')],
        'achievements': ['Reduced hiring time by 20%'],
        'languages': [('English', 'Fluent'), ('Hindi', 'Native')],
    },
    'minimal-3': {
        'template': 'minimal', 'label': 'Minimal — Graphic Designer',
        'title': 'Graphic Designer Resume',
        'name': 'Arjun Das', 'email': 'arjun.das@email.com', 'phone': '+91 96543 21098',
        'location': 'Kolkata, India', 'linkedin': 'https://linkedin.com/in/arjundas', 'github': '',
        'summary': 'Graphic designer with a strong visual sense, experienced in branding, print, and digital design for startups.',
        'education': [('B.Des in Visual Communication', 'Srishti Institute', '2019-2023', '8.3 CGPA')],
        'experience': [('CreativeHive', 'Graphic Designer', 'Aug 2023 - Present', 'Designed brand identities and marketing collateral for 10+ startup clients.')],
        'skills': ['Photoshop', 'Illustrator', 'InDesign', 'Branding', 'Typography'],
        'projects': [('Startup Rebrand Series', 'Delivered full brand identity kits for 5 early-stage startups.', 'Illustrator, Figma', '')],
        'certifications': [('Adobe Certified Professional', 'Adobe', '2022')],
        'achievements': ['Designed identity for award-winning startup'],
        'languages': [('English', 'Fluent'), ('Bengali', 'Native')],
    },
}


@login_required
def sample_gallery(request):
    return render(request, 'resumes/sample_gallery.html', {'samples': SAMPLE_RESUMES})


@login_required
def use_sample_resume(request, sample_key):
    data = SAMPLE_RESUMES.get(sample_key)
    if not data:
        return redirect('sample_gallery')

    resume = Resume.objects.create(user=request.user, title=data['title'], template=data['template'])
    PersonalInfo.objects.create(
        resume=resume, full_name=data['name'], email=data['email'], phone=data['phone'],
        location=data['location'], linkedin=data['linkedin'], github=data['github'], summary=data['summary']
    )
    for degree, institution, year, score in data['education']:
        Education.objects.create(resume=resume, degree=degree, institution=institution, year=year, score=score)
    for company, role, duration, description in data['experience']:
        Experience.objects.create(resume=resume, company=company, role=role, duration=duration, description=description)
    for skill in data['skills']:
        Skill.objects.create(resume=resume, name=skill)
    for title, description, tech_stack, link in data['projects']:
        Project.objects.create(resume=resume, title=title, description=description, tech_stack=tech_stack, link=link)
    for name, issuer, year in data['certifications']:
        Certification.objects.create(resume=resume, name=name, issuer=issuer, year=year)
    for title in data['achievements']:
        Achievement.objects.create(resume=resume, title=title)
    for name, proficiency in data['languages']:
        Language.objects.create(resume=resume, name=name, proficiency=proficiency)

    return redirect('edit_resume', resume_id=resume.id)