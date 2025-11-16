from rest_framework import serializers
from .models import Questions, LotteryList, GoldCard
from accounts.models import CustomUser
from django.utils import timezone
from datetime import timedelta
import random

class QuestionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questions
        fields = ['id', 'question', 'answer1', 'answer2', 'amount']

class AnswerQuestionSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()
    selected_answer = serializers.ChoiceField(choices=[('1','answer1'),('2','answer2')])

    def validate(self, attrs):
        user = self.context['request'].user
        question_id = attrs.get('question_id')

        try:
            question = Questions.objects.get(id=question_id, is_active=True)
        except Questions.DoesNotExist:
            raise serializers.ValidationError("سوال یافت نشد یا فعال نیست.")

        if LotteryList.objects.filter(user=user, question=question).exists():
            raise serializers.ValidationError("شما قبلاً به این سوال پاسخ داده‌اید.")

        attrs['question'] = question
        return attrs

    def save(self):
        user = self.context['request'].user
        question = self.validated_data['question']
        selected = self.validated_data['selected_answer']

        correct = (selected == question.correct_answer)

        if correct:
            gold_card = GoldCard.objects.filter(user=user, question=question).first()
            if not gold_card:
                while True:
                    serial = ''.join([str(random.randint(0,9)) for _ in range(16)])
                    if not GoldCard.objects.filter(serial=serial).exists():
                        break

                expire_date = timezone.now() + timedelta(days=30)

                gold_card = GoldCard.objects.create(
                    user=user,
                    question=question,
                    serial=serial,
                    expire_date=expire_date
                )

            LotteryList.objects.create(user=user, question=question, gold_card=gold_card)

        return correct
