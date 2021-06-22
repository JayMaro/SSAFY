# 예외처리!
#  평균을 내는 함수!
# def _avg(scores):
#     try:
#         # 실행하다가
#         return sum(scores) / len(scores)
#     # 특정한 오류가 발생하면
#     except ZeroDivisionError:
#         # 행동!
#         return 0
class NoTestError(ZeroDivisionError):
    pass
def _avg(scores):
    if len(scores) == 0:
        raise NoTestError('시험 안본 학생이 있습니다.')
    return sum(scores) / len(scores)
# 위의 함수를 활용해서 학생들의 각각 평균을 출력하는 함수!
def class_avg(students):
    for scores in students.values():
        print(_avg(scores))
