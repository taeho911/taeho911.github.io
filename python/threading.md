# Threading of Python

## 파이썬의 GIL
파이썬은 멀티쓰레딩을 지원하지만 동시에 실행가능한 쓰레드는 하나뿐이다.
그 이유는 GIL(Global Interpreter Lock) 때문이다.

파이썬은 멀티쓰레딩시, 공유자원에 대한 개별적 락을 하지 않고, 인터프리터 자체에 락을 걸어버린다.
이 때문에 파이썬의 동시 실행 가능한 쓰레드는 단 한가지뿐이다.
공유자원에 개별적 락을 걸지 않는 이유는 데드락 혹은 반복되는 락/해제로 인한 성능저하 같은 사이드 이펙트를 회피하기 위함이다.
(Ruby와 같이 인터프리터를 쓰는 다른 언어는 reference counting garbage collection과는 다른 thread-safe memory management를 통해 GIL을 회피하고 있다.)

## 왜 파이썬은 GIL을 선택했는가?
Larry Hastings에 의하면 파이썬은 운영체제에 쓰레드라는 개념이 일반화되지 이전(1970년대)부터 존재해왔으며(1980년대 후반), 기존의 non-thread-safe C 라이브러리를 다수 이용하기 위해 쓰레드를 안전하게 다룰 방법이 필요했다.
이 때문에 GIL을 선택하게 되었다고 한다.

## 파이썬은 왜 아직도 GIL을 이용하고 있는가?
과거에 파이썬에서 GIL을 없애는 프로젝트들이 있었으나, 그 결과는 GIL에 크게 의존하던 C extentions들의 호환성을 깨뜨리게 되었으며, 이를 회피하더라도 GIL에 비해 성능이 저하되는 경향이 있었다고 한다.

## 파이썬이 멀티쓰레딩을 하면 구체적으로 어떻게 되는가?
CPU코어가 몇개가 있던 파이썬이 멀티쓰레딩을 할 경우 CPU 사용률이 100%를 넘어가지 않는다.
다른 언어의 경우 CPU 집적인 작업을 쓰레딩할 경우 CPU 사용률이 정상적으로 200%, 300% 등으로 올라가는 것과는 상반된다.

## 그렇다면 파이썬의 멀티쓰레딩은 쓸모가 없는가?
그렇지 않다.
IO 작업의 경우에는 오버헤드가 요청/응답의 오버헤드가 발생하기에 GIL에 의한 멀티쓰레딩이라도 전체적인 성능을 향상시켜주는 유효타가 된다.
반면 CPU 집적인 작업의 경우에는 그렇지 못한 경우가 많다.

## 파이썬에서 CPU 집적인 작업을 병렬처리하려면 어찌해야 하는가?
multiprocessing을 쓰면된다.
다만 multiprocessing의 경우 기본적으로 메모리를 공유하지 않기에 공유메모리를 만들고 여기에 데이터를 읽기/쓰기를 하며 프로세스간의 소통을 도모해야 한다.
또한 multiprocessing에서의 공유자원도 락이 필요한 것은 매한가지라 완전히 제약에서 자유롭지는 못하다.
그럼에도 불구하고 CPU 집적인 작업에서는 multi-threading보다 유효하다.
