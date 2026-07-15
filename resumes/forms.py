from django import forms
from django.forms import inlineformset_factory
from .models import Resume, PersonalInfo, Education, Experience, Skill, Project, Certification, Achievement, Language


class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['title', 'template']


class PersonalInfoForm(forms.ModelForm):
    class Meta:
        model = PersonalInfo
        fields = ['full_name', 'email', 'phone', 'location', 'linkedin', 'github', 'summary']


class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['degree', 'institution', 'year', 'score']


class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ['company', 'role', 'duration', 'description']


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name']


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'tech_stack', 'link']


class CertificationForm(forms.ModelForm):
    class Meta:
        model = Certification
        fields = ['name', 'issuer', 'year']


class AchievementForm(forms.ModelForm):
    class Meta:
        model = Achievement
        fields = ['title']


class LanguageForm(forms.ModelForm):
    class Meta:
        model = Language
        fields = ['name', 'proficiency']


EducationFormSet = inlineformset_factory(
    Resume, Education,
    form=EducationForm,
    extra=1, can_delete=True
)

ExperienceFormSet = inlineformset_factory(
    Resume, Experience,
    form=ExperienceForm,
    extra=1, can_delete=True
)

SkillFormSet = inlineformset_factory(
    Resume, Skill,
    form=SkillForm,
    extra=1, can_delete=True
)

ProjectFormSet = inlineformset_factory(
    Resume, Project,
    form=ProjectForm,
    extra=1, can_delete=True
)

CertificationFormSet = inlineformset_factory(
    Resume, Certification,
    form=CertificationForm,
    extra=1, can_delete=True
)

AchievementFormSet = inlineformset_factory(
    Resume, Achievement,
    form=AchievementForm,
    extra=1, can_delete=True
)

LanguageFormSet = inlineformset_factory(
    Resume, Language,
    form=LanguageForm,
    extra=1, can_delete=True
)