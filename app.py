from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

DB_PATH = r"C:\Users\arsuser\Documents\anime_project\anime.db"

def search_db(birthday):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT name, anime, birthday, image
    FROM characters
    WHERE birthday = ?
    LIMIT 10
    """, (birthday,))

    results = cursor.fetchall()
    conn.close()
    return results

def get_day_info(birthday):
    data = {
        "01-01": "元日",
        "02-03": "節分",
        "02-14": "バレンタインデー",
        "03-03": "ひな祭り",
        "04-01": "エイプリルフール",
        "05-05": "こどもの日",
        "07-07": "七夕",
        "08-11": "山の日",
        "10-31": "ハロウィン",
        "12-24": "クリスマスイブ",
        "12-25": "クリスマス",
        "12-31": "大晦日"
    }

    return data.get(birthday, "この日の情報はまだ登録されていません。")

def get_event_info(birthday):
    data = {
        "01-01": "日本では新しい年の始まりとして、多くの人が初詣に行きます。",
        "02-03": "節分では豆まきを行い、無病息災を願います。",
        "02-14": "バレンタインデーとして、チョコレートを贈る文化があります。",
        "03-03": "ひな祭りとして、女の子の健やかな成長を願います。",
        "04-01": "新年度の始まりであり、多くの学校や会社で新しい生活が始まります。",
        "05-05": "こどもの日として、子どもの成長と幸せを願います。",
        "07-07": "七夕として、短冊に願い事を書きます。",
        "08-11": "山の日として、山や自然に親しむ日です。",
        "10-31": "ハロウィンとして、仮装やイベントが行われます。",
        "12-24": "クリスマスイブとして、家族や友人と過ごす人が多い日です。",
        "12-25": "クリスマスとして、世界中で祝われる日です。",
        "12-31": "大晦日として、一年の終わりを迎える日です。"
    }

    return data.get(birthday, "この日に起こった出来事はまだ登録されていません。")

def generate_story(results):
    if len(results) == 0:
        return "キャラクターが見つからないため、ストーリーを生成できません。"

    if len(results) == 1:
        name = results[0][0]
        return f"{name}は自分と同じ誕生日の仲間を探すため、新しい冒険へ出発しました。"

    name1 = results[0][0]
    name2 = results[1][0]

    return f"{name1}と{name2}は同じ誕生日だと知り、特別な一日を一緒に過ごすことになりました。二人はお互いの世界について話し合い、新しい友情を築きました。"

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    searched = False
    day_info = ""
    event_info = ""
    story = ""

    if request.method == "POST":
        birthday = request.form["birthday"].strip()
        searched = True

        results = search_db(birthday)
        day_info = get_day_info(birthday)
        event_info = get_event_info(birthday)
        story = generate_story(results)

    return render_template(
        "index.html",
        results=results,
        searched=searched,
        day_info=day_info,
        event_info=event_info,
        story=story
    )

if __name__ == "__main__":
    app.run(debug=True)

