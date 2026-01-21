const peopleSections = document.querySelectorAll('.person');
const speechBubbles = document.querySelectorAll('.speech-bubble');

// 預先定義每個人的話
const speeches = {
    person1: "歡迎來到吉祥島。我是靜雅，這座島的市長。\n這裡的每一條道路、每一座神像、每一個禁區，都經過我的批准與記錄。\n你可以放心探索——前提是，你能承擔後果。Welcome to AuspiceIsle.I'm Alicia, the mayor of this island.Every road, every monument, every restricted zone—was approved and archived by me.",
    person2: "大家好，我是人物二，很高興來到這裡。",
    person3: "嗨！我是人物三，很高興為你服務！",
    person4: "嗨！我是人物三，很高興為你服務！",
    person5: "嗨！我是人物三，很高興為你服務！",
    person6: "嗨！我是人物三，很高興為你服務！",
    person7: "嗨！我是人物三，很高興為你服務！"


    // 可以為更多人物添加對應的話
};

peopleSections.forEach(person => {
    const name = person.dataset.name;
    const bubble = person.querySelector('.speech-bubble');
    if (bubble && speeches[name]) {
        bubble.textContent = speeches[name];

        // 移除 click 事件監聽器
        // person.addEventListener('click', function() {
        //     this.classList.toggle('active'); // 切換 active class 來顯示/隱藏 speech-bubble

        //     // 點擊時，隱藏其他人的 speech bubble
        //     peopleSections.forEach(otherPerson => {
        //         if (otherPerson !== this && otherPerson.classList.contains('active')) {
        //             otherPerson.classList.remove('active');
        //         }
        //     });
        // });

        // 新增 mouseenter 事件監聽器
        person.addEventListener('mouseenter', function() {
            this.classList.add('active'); // 滑鼠移上去時，顯示 speech-bubble

            // 顯示這個人的 speech bubble 時，隱藏其他人的
            peopleSections.forEach(otherPerson => {
                if (otherPerson !== this) {
                    otherPerson.classList.remove('active');
                }
            });
        });

        // 新增 mouseleave 事件監聽器
        person.addEventListener('mouseleave', function() {
            this.classList.remove('active'); // 滑鼠移開時，隱藏 speech-bubble
        });
    }
});