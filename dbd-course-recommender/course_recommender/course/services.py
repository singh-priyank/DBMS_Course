import random

import numpy as np
import pandas as pd
from pandas import DataFrame
from rake_nltk import Rake
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from users.models import Student

from .models import *
def get_recommendations_cf(uid):
    subs = get_enrolled_subjects(uid)
    if len(subs) == 0:
        recommmend_list = random.choices(list(Course.objects.all()), k=min(len(list(Course.objects.all())),10))
    else:
        l1=[]
        cats=[sub.course.category for sub in subs]
        for cat in cats:
            l1 += list(Course.objects.filter(category = cat))
            l1=list(set(l1))
        l2=[]
        for sub in subs:
            l2 +=list(Course.objects.filter(instructor = sub.course.instructor))
            #l2 +=list(Course.objects.filter(cost = sub.cost))
            l2 +=list(Course.objects.filter(platform = sub.course.platform))
            l2 +=list(Course.objects.filter(language = sub.course.language))
            l2 +=list(Course.objects.filter(level = sub.course.level))
            l2=list(set(l2))
        recommmend_list = random.choices(list(set(l1+l2)), k=min(len(list(set(l1+l2))),10))


def get_recommmendations(user):
    is_valid, enrolled_subjects = _validate(user)
    if is_valid:
        recommendations = _from_content_based(enrolled_subjects)
    else:
        recommendations = _from_random()
    return recommendations


def _validate(user):
    is_valid = False
    enrolled_subjects = []
    if user.is_authenticated:  # atuthenticated user
        enrolled_subjects = get_enrolled_subjects(user.id).values_list('course', flat=True)
        if enrolled_subjects.count() >= 1:
            is_valid = True
    return is_valid, enrolled_subjects


def _from_random():
    subjects_size = Course.objects.count()
    random_list = random.sample(range(0, subjects_size), 3)
    recommendations = _retrieve_recommendations_and_sort_by(random_list)
    return recommendations


def _from_content_based(subject_list):
    df = DataFrame(list(Course.objects.values('name', 'category__name')))

    df = _data_clean(df, subject_list)
    
    # instantiating and generating the count matrix
    count = CountVectorizer()
    count_matrix = count.fit_transform(df['key_words'])
    # generating the cosine similarity matrix
    cosine_sim = cosine_similarity(count_matrix, count_matrix)

    rd_list, rating = _recommendations(subject_list, df, cosine_sim)

    recommendations = _retrieve_recommendations_and_sort_by(rd_list)

    _calculate_ratings(rd_list, df, cosine_sim)
    
    return recommendations


def _data_clean(dataframe, subject_list):
    enrolled_key_words = ""
    dataframe['name_keywords'] = ""
    for index, row in dataframe.iterrows():
        name = row['name']
        r = Rake()
        r.extract_keywords_from_text(name)
        keywords_dict = r.get_word_degrees()
        name_keywords_str = ' '.join(list(keywords_dict.keys()))
        row['name_keywords'] = name_keywords_str
        if index+1 in subject_list:
            enrolled_key_words += name_keywords_str + " " + row['category__name'] + " "
    dataframe['key_words'] = dataframe['name_keywords'] + ' ' + dataframe['category__name'].map(str)
    dataframe = dataframe.append({'key_words': enrolled_key_words}, ignore_index=True)
    
    return dataframe


def _recommendations(subject_list, df, cosine_sim):
    enrolledIndex = df.shape[0] - 1
    indices = pd.Series(df.index)

    # initializing the empty list of recommended subjects
    recommended_subjects = []

    # gettin the index of the subject that matches the id
    idx = indices[indices == enrolledIndex].index[0]
    
    # creating a Series with the similarity scores in descending order
    score_series = pd.Series(cosine_sim[idx]).sort_values(ascending=False)
    

    # select top 10 recommended subjects that are not in the enrolled subject list
    real_sims = []
    sum_of_product = 0
    sum_of_sims = 0
    for items in score_series.iteritems():
        if len(recommended_subjects) > 9:
            break
        indx = items[0]
        real_sim = items[1]
        if indx is not enrolledIndex:
            subjectId = indx + 1
            if subjectId not in subject_list:
                recommended_subjects.append(subjectId)
                real_sims.append(real_sim)
                subject_name = Course.objects.get(id=subjectId)
                rating_list = SubjectRating.objects.filter(subject = subject_name).values_list('rating', flat=True)
                if(rating_list.count() > 0):
                    average_rating = sum(rating_list) / rating_list.count()
                else:
                    average_rating = 0
                sum_of_product += real_sim * average_rating
                sum_of_sims+=real_sim
                if(sum_of_sims > 0):
                    rating = sum_of_product / sum_of_sims
                else:
                    rating = 0

    '''
    print(real_sims)
    print(rating)
    #evaluation()'''
    return recommended_subjects, rating

def _retrieve_recommendations_and_sort_by(subject_list):
    # return detailed information of recommendation list
    recommendations = list(Course.objects.filter(pk__in=subject_list).values())
    recommendations.sort(key=lambda t: subject_list.index(t['id']))
    return recommendations


def _calculate_ratings(rd_list, df, cosine_sim):
    index=0
    single_list = []
    rating_list = []
    for subject in rd_list:
        single_list.append(rd_list[index]) 
        tmp_list, rating = _recommendations(single_list, df, cosine_sim)
        rating_list.append(rating)
        index +=1
    rating_series = pd.Series(rd_list, index=rating_list)

def get_enrolled_subjects(userId):

    current_student = Student.objects.get(account=userId)
    enrolled_course_list = Enrollment.objects.filter(
        student=current_student.id)
    return enrolled_course_list

def get_recommendations_cf(uid):
    subs = get_enrolled_subjects(uid)
    if len(subs) == 0:
        recommmend_list = random.choices(list(Course.objects.all()), k=min(len(list(Course.objects.all())),10))
    else:
        l1=[]
        cats=[sub.course.category for sub in subs]
        for cat in cats:
            l1 += list(Course.objects.filter(category = cat))
            l1=list(set(l1))
        l2=[]
        for sub in subs:
            l2 +=list(Course.objects.filter(instructor = sub.course.instructor))
            #l2 +=list(Course.objects.filter(cost = sub.cost))
            l2 +=list(Course.objects.filter(platform = sub.course.platform))
            l2 +=list(Course.objects.filter(language = sub.course.language))
            l2 +=list(Course.objects.filter(level = sub.course.level))
            l2=list(set(l2))
        recommmend_list = random.choices(list(set(l1+l2)), k=min(len(list(set(l1+l2))),10))
    return recommmend_list