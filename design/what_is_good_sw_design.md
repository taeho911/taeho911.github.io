# Software Design Principles
https://www.youtube.com/watch?v=bmSAYlu0NcY
Presented by John Ousterhout, Professor of Computer Science at Stanford University

## Classes Should be Deep
클래스를 구성하는 인터페이스는 유저들에게 있어서 해당 클래스를 사용하기 위해 기억해야하는 룰이기에 코스트로 생각할 수 있다.
반면 클래스가 제공하는 다양한 유틸리티 함수들은 베네핏으로 생각할 수 있다.
이러한 관점에서 좋은 클래스는 되도록 작은 인터페이스를 가지고 많은 유틸리티를 제공할 수 있어야 한다.(Deep class)
우리는 가끔 이러한 함수들을 보게 된다.

```
private void addNullValueForAttribute(String attr) {
    data.put(attr, null)
}
```

위와 같은 함수는 유저에게 전혀 유용성을 제공하지 못하며 단지 프로그램에 인터페이스(코스트)를 추가할 뿐이다.(Shellow class)
추상화라는 관점에서 위와 같은 메소드나 클래스의 정의는 피하는것이 좋다.
Java 생태계에서는 클래스나 메소드를 되도록 작은 단위로 쪼개는 것이 바람직하다는 문화가 넓게 퍼지면서 인터페이스들에 대한 복잡도는 증가하고 이로인해 유저들이 얻을 수 있는 유용성은 줄어들어 왔다.
단적인 예가 아래와 같은 File IO 클래스들이다.

```
FileInputStream fs = new FileInputStream(filename);
BufferedInputStream bs = new BufferedInputStream(fs);
ObjectInputStream os = new ObjectInputStream(bufferedStream);
```

파일 하나를 조작하기 위해 3개의 오브젝트를 생성해야 한다.

## Define Errors Out of Existence
예외처리는 프로그램의 복잡도를 올리는 주범중 하나다.
이러한 예외처리에 대한 미신중 하나가 *_되도록 많은 예외를 감지하고 던져라_*이다.
모든 예외를 감지하고 처리할때 안심감과 뿌듯함을 느끼는 프로그래머들이 존재한다.
하지만 정말 좋은 예외처리 방식은 프로그램이 사용되는 방식을 이해하여 예외처리를 할 필요가 없도록 하는 것이다.

예를 들어 unset을 생각해보자.
만약 unset이 존재하지 않는 변수를 대해 매번 예외를 던진다면 사용하기가 무척 불편해질 것이다.
유저가 unset을 통해 얻고자하는 것은 해당 변수가 사라지는 것이지, 해당 변수가 존재하는지 존재하지 않는지를 알기 위함이 아니다.

## Tactical vs Strategic Programming
텍티컬 프로그래밍의 주목적은 가능한 발빠르게 *_작동하는 프래그램_*을 만드는 것이다.
하지만 텍티컬 프로그래밍은 프로그램의 복잡도를 증가시키고 결국 나쁜 디자인으로 귀결되는 경우가 많다.(스파게티 코드)
반면 스트레터직 프로그래밍의 주목적은 좋은 디자인으로 복잡도를 줄이면서 *_좋은 프로그램_*을 만드는 것이다.
스트레터직 프로그래밍은 초기에는 텍티컬 프로그래밍보다 개발 속도가 느리지만 프로그램이 점점 커질수록 텍티컬 프로그래밍보다 생산적이게 된다.

John에 의하면 이러한 스트레터직 프로그래밍에 투자되어야하는 오버헤드는 10~20% 정도라고 한다.
예를 들어 전체 개발기간이 3개월이라고 한다면 열흘 정도는 어떻게 더 좋은 디자인으로 프로그램을 만들까 고민하고 실행하는데 써야한다는 것이다.
