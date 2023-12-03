class Participant:
    """参加者"""

    def __init__(self, id: int) -> None:
        self._id = id
        self._encountered: list["Participant"] = []

    def encounter(self, other: "Participant") -> None:
        """他の参加者と出会う"""
        self._encountered.append(other.id)

    def has_encountered(self, other: "Participant") -> bool:
        """他の参加者と出会ったことがあるかどうかを判定する"""
        return other.id in self._encountered

    @property
    def id(self) -> int:
        return self._id


class Seminar:
    """セミナー"""

    def __init__(self, participants_count: int) -> None:
        """コンストラクタ

        Args:
            participants_count (int): 参加者数
        Errors:
            ValueError: 参加者数が0以下の場合"""
        if participants_count <= 0:
            raise ValueError("Participants count must be positive")
        self._participants: list[Participant] = []
        for i in range(participants_count):
            self._participants.append(Participant(i))

    def make_teams(self, teams_count: int) -> list[list[Participant]]:
        """チーム分けを行う

        すべての参加者がまだ出会っていない参加者と一緒になるようにチームを作る

        Args:
            teams_count (int): チーム数
        Errors:
            ValueError: チーム数が参加者数より多い場合
            ValueError: 参加者数がチーム数で割り切れない場合
            Error: 全ての参加者がまだ出会っていない参加者と一緒になるチームを作成できない場合
        """
        if teams_count > len(self._participants):
            raise ValueError("Not enough participants")
        if len(self._participants) % teams_count != 0:
            raise ValueError("Cannot make even teams")
        teams: list[list[Participant]] = [[] for _ in range(teams_count)]
        for p in self._participants:
            for t in teams:
                if any(p.has_encountered(other) for other in t):
                    continue
                if len(t) == len(self._participants) // teams_count:
                    continue
                for other in t:
                    p.encounter(other)
                    other.encounter(p)
                t.append(p)
                break
            else:
                raise RuntimeError(
                    f"The participant {p.id} cannot be assigned to any team"
                )
        return teams


if __name__ == "__main__":
    print("セミナーを開催します。")
    while not (participants_count := input("参加者数を入力してください: ")).isnumeric():
        pass
    participants_count = int(participants_count)
    seminar = Seminar(participants_count)
    print("チーム分けを行います。")
    while not (teams_count := input("チーム数を入力してください: ")).isnumeric():
        pass
    teams_count = int(teams_count)
    iteration_count = 0
    while True:
        iteration_count += 1
        try:
            teams = seminar.make_teams(teams_count)
            print("*", end="")
        except Exception as e:
            print(f"\n{iteration_count - 1}回チーム分けを行えました。")
            break
    print("--------------------")
    common_divisors = [
        i
        for i in range(1, min(participants_count, teams_count) + 1)
        if participants_count % i == 0 and teams_count % i == 0
    ]
    print(f"{participants_count}と{teams_count}の公約数は{len(common_divisors)}個あります。")
    print(common_divisors)
