from django.db.models import Count


def annotate_comments_queryset(querryset):
    return querryset.annotate(comment_count=Count('comments'))
