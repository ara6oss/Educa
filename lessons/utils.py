from django.db.models import Q
from lessons.models import Lesson
from django.contrib.postgres.search import (
    SearchVector,
    SearchQuery,
    SearchRank,
    SearchHeadline,
)


def q_search(query):

    vector = SearchVector("title")
    # vector = SearchVector("title", "overview")
    query = SearchQuery(query)

    result = (
        Lesson.objects.annotate(rank=SearchRank(vector, query))
        .filter(rank__gt=0)
        .order_by("-rank")
    )
    result = result.annotate(
        headline = SearchHeadline(
            "title",
            query,
            start_sel='<span style="background-color: yellow;">',
            stop_sel='</span>',
        )
    )
    # result = result.annotate(
    #     bodyline=SearchHeadline(
    #         "overview",
    #         query,
    #         start_sel='<span style="background-color: yellow;">',
    #         stop_sel='</span>',
    #     )
    # )
    print(result)
    return result