import random

import numpy as np  # linear algebra
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from .services import get_enrolled_subjects, get_recommmendations
from .models import *
from .services import (_from_random, _retrieve_recommendations_and_sort_by,
                       _validate)

def get_recommendations(uid):
    subs = get_enrolled_subjects(uid)
    if len(subs) == 0:
        recommmend_list = list(Course.objects.all())
    else:
        l1=[]
        cats=[sub.course.category for sub in subs]
        for cat in cats:
            l1 += list(Course.objects.filter(category = cat))
            l1=list(set(l1))
        l2=[]
        for sub in subs:
            l2 +=list(Course.objects.filter(instructor = sub.course.instructor))
            l2 +=list(Course.objects.filter(cost = sub.course.cost))
            l2 +=list(Course.objects.filter(platform = sub.course.platform))
            l2 +=list(Course.objects.filter(language = sub.course.language))
            l2 +=list(Course.objects.filter(level = sub.course.level))
            l2 +=list(Course.objects.filter(certificate = sub.course.certificate))
            l2=list(set(l2))
        recommmend_list = list(set(l1+l2))
    return recommmend_list


def get_recommmendations_cf(user):
    is_valid, enrolled_subjects = _validate(user)
    if is_valid:
        recommendations = _from_collaborative_filtering(enrolled_subjects)
    else:
        recommendations = _from_random()
    return recommendations


def _from_collaborative_filtering(enrolled_subjects):
    ratings = pd.DataFrame(
        list(SubjectRating.objects.values()))  # .values('rating')

    enrolledSubjectId = enrolled_subjects[len(enrolled_subjects)-1]

    # subjects=pd.DataFrame(list(Subject.objects.values()))#.values( 'lecture')
    # print(subjects.head(15))

    # subject_ratings = pd.merge(subjects, ratings)
    # print(subject_ratings.head(15))

    ratings_matrix = ratings.pivot_table(index=['subject_id'], columns=[
                                         'student_id'], values='rating').reset_index(drop=True)
    ratings_matrix.fillna(0, inplace=True)

    subject_similarity = cosine_similarity(ratings_matrix)
    np.fill_diagonal(subject_similarity, 0)

    ratings_matrix = pd.DataFrame(subject_similarity)

    # initializing the empty list of recommended subjects
    recommended_subjects = []

    score_series = pd.Series(
        subject_similarity[0]).sort_values(ascending=False)

    # select top 10 recommended subjects that are not in the enrolled subject list
    for items in score_series.iteritems():
        if len(recommended_subjects) > 9:
            break
        indx = items[0]
        subjectId = indx + 1
        if subjectId not in enrolled_subjects:
            recommended_subjects.append(subjectId)

    recommendations = _retrieve_recommendations_and_sort_by(
        recommended_subjects)
    return recommendations
