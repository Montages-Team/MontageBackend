from django.core.exceptions import ObjectDoesNotExist

from accounts.models import MontageUser
from portraits.models.questions import Question
from portraits.models.impressions import Impression

import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField


class ImpressionType(DjangoObjectType):
    """ImpressionType."""

    class Meta:
        """Meta."""
        model = Impression


class UserImpressionsType(DjangoObjectType):

    class Meta:
        """Meta."""
        model = Impression
        # filter_fields = {
        #     'user.username': ["exact"],
        # }
        # interfaces = (graphene.Node, )


class CreateImpressionMutation(graphene.Mutation):
    """
    Impressionの作成

    IN
    ------
    mutation{
      createImpression(userId: 1, questionId: 22, content: "質問への回答"){
        impression{
          id
          question{
            about
          }
          content
        }
      }
    }
    """
    impression = graphene.Field(ImpressionType)
    ok = graphene.Boolean()

    class Input:
        question_id = graphene.Int(required=True)
        user_id = graphene.Int(required=True)
        content = graphene.String(required=True)

    def mutate(self, info, question_id, user_id, content):
        # イジられる側のユーザ
        user_id = user_id
        ok = True

        try:
            # イジられる側のユーザを取得
            user = MontageUser.objects.get(id=user_id)
        except ObjectDoesNotExist:
            ok = False

        question = Question.objects.get(id=question_id, user=user)

        impression = Impression.objects.create(
            user=user, question=question, content=content)
        impression.save()
        return CreateImpressionMutation(impression=impression, ok=ok)


class DeleteImpressionMutation(graphene.Mutation):
    """
    Impressionの削除

    IN
    ------
    mutation{
      deleteImpression(id: 4){
        id
      }
    }

    OUT
    ----
    {
      "data": {
        "deleteImpression": {
          "id": 4
        }
      }
    }
    """
    ok = graphene.Boolean()

    class Arguments:
        id = graphene.Int()

    def mutate(self, info, id):
        try:
            Impression.objects.filter(id=id).delete()
            ok = True
        except ObjectDoesNotExist:
            ok = False

        return DeleteImpressionMutation(id=id, ok=ok)


class Mutation(graphene.ObjectType):
    create_impression = CreateImpressionMutation.Field()
    delete_impression = DeleteImpressionMutation.Field()


class Query(graphene.ObjectType):
    impression = graphene.Field(ImpressionType, question=graphene.String())
    impressions = graphene.List(ImpressionType)
    user_impressions = graphene.List(UserImpressionsType, username=graphene.String())

    def resolve_impression(self, question, info):
        return Impression.objects.get(question=question)

    def resolve_impressions(self, info):
        return Impression.objects.all()

    def resolve_user_impressions(self, info, username):
        """ユーザ毎の回答済みimpressionsを取得するときのクエリ結果


        Notes
        ----------
        IN
        query{
          userImpressions(username: "RAGUNA2"){
            id
            question{
              id
              about
            }
            content
          }
        }

        OUT
        {
          "data": {
            "userImpressions": [
              {
                "id": "4",
                "question": {
                  "id": "1",
                  "about": "性別は?"
                },
                "content": "男"
              },
              ...
            ]
          }
        }
        """
        user = MontageUser.objects.get(username=username)
        return Impression.objects.filter(user=user)
