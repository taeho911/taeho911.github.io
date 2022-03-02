# Why is Python's Running Speed Slow

## The Way How Python Run the Code
우리가 파이썬 코드를 작성하여 이를 파이썬으로 돌릴때 아래와 같은 단계를 거쳐 코드가 실행된다.

1. Compile .py code into bytecode which can be run by python interpret. (.pyc를 생성한다.)
2. Python interpreter(PVM) reads the bytecode, changes it to machine code and runs the code.

모든 언어은 특정 운영체제에서 프로그램을 돌려야하기 때문에 결국엔 머신코드를 생성할 수 밖에 없다.
하지만 머신코드로 변환되기 전 단계인 바이트코드가 얼마나 정교하게 컴파일되느냐에 따라 해당 언어의 실행 속도가 달라지곤 한다.

## Dynamic Typing
Java의 경우 파이썬과 비슷한 방식을 통해 코드가 실행되지만 파이썬과는 다르게 정적으로 타입을 정의하는 언어이다.
때문에 컴파일 단계에서 이미 각 변수에 할당되어야하는 메모리의 크기를 알 수 있으며, 이를 베이스로 코드의 최적화를 하거나 더 저수준에 가까운 바이트 코드로 컴파일하는 것이 가능하다.
반면에 파이썬은 동적으로 타입을 평가하기 때문에 컴파일 단계에서의 최적화가 제한될 수 밖에 없으며 바이트 코드의 수준에 고수준에 머무를 수 밖에 없다.
또한 동적 타입 평가이기에 런타임에 해당 변수의 타입을 평가하여 추적하는 과정이 필요하게 된다.
이러한 차이는 파이썬 코드의 실행속도를 저하하는 근본적인 이유가 된다.

## How Could We Speed Up Python Code?
파이썬은 C extention을 지원한다.
이를 사용하여 프로그래밍을 할 경우 C코드 수준으로 코드가 컴파일되기에 기존의 파이썬 코드와 비교하여 굉장히 빠른 속도로 코드를 실행할 수 있다.
대표적인 예가 numpy이다.
