<template>
  <div class="home-page">
    <div class="header">
      <icon-content icon-name='setting1' content="设置" @click.native="setting" />
      <span>Snipaste OCR</span>
      <div>
        <icon-content icon-name='zuixiaohua' content="最小化" @click.native="minimize" />
        <icon-content icon-name='tuichu' content="退出" @click.native="quit" />
      </div>
    </div>
    <div class="body">
      <div class="aside">
        <div class="histories">
          <div :class="historyItem(index)" v-for="(history,index) in histories" :key='index' @click="selectHistory(index)">
            <h3>{{datetime(history.date,history.time)}}</h3>
            <p>{{simpleWord(history.ocrResult)}}</p>
            <icon-content icon-name='delete' class="history-delete"></icon-content>
          </div>
        </div>

        <button class="ocr-btn" @click="ocr">
          <icon-content icon-name='jieping' class="ocr-icon"></icon-content>
          OCR一下
        </button>
      </div>
      <div class="main">
        <div class="resultHeader">
          <h2>{{ datetime(histories[selectIndex].date,histories[selectIndex].time)}}</h2>
          <div class="underline"></div>
        </div>
        <div class="resultBody">
          <div class="result">
            <h4>OCR识别结果:</h4>
            <icon-content icon-name='lujing182' class="copy" content="复制" position='right'></icon-content>
            <p class="ocrResult">{{ histories[selectIndex].ocrResult }}</p>
          </div>
          <div class="source">
            <h4>原图:</h4>
            <div class="img">
              <img :src="histories[selectIndex].ocrImgUrl" alt="">
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import IconContent from "@/components/common/IconContent/index";
import request from "@/util/request.js";
const {ipcRenderer: ipc} = require("electron");
export default {
  name: "HomePage",
  components: {IconContent},
  data() {
    return {
      histories: [
        {
          date: "2020-08-25",
          time: "12:05:06",
          ocrResult: `一、引言*

1.1 从体验经济到体验设计。

随着社会生产力发展水平的提高和人类需求层次的升级，体验经济世就成
为了经济发展的必然趋势。体验经济日渐显现，出现了服务于它的体验设计。…

设计是包押的重要组成部分。在强调自主创新的大环境下，中国的企业应
该充分关注体验设计的新趋势体验设计的理论正在成为现代企业开发产品和
服务项目的重要依据。现阶段，IT 领域很早就注意到了这一点，百度、腾讯、
支付宝, 阿里巴巴等都设有专门的用户体验部, 为其产品和服务增加附加价值，
也更大程度地让用户满意，最终获得了最佳企业效益。"

同时，随着现代产品设计思想的成熟，产品设计也赤来越聚焦于人本身一
一人的存在，人的需要，特别是人的情感需要。设计与人，人与设计，设计是
否可以有长远意义, 是否可以印证人的真实存在, 是否可以帮助人们理解自己，
认识世界。这个问题已偏向于哲学, 但却确实是设计这种文化形式的内在诉求。
越来越多的产品通过设计，在与人交互的过程中，使人产生以悦的体验，并在
这个体验的后期，让人产生反思，通过反思得以认识自己发展自己。我想这
点是设计成为一种优势文化，而所要肩负的必要责任。"`,
          ocrImgUrl:
            "https://ss0.bdstatic.com/70cFuHSh_Q1YnxGkpoWK1HF6hhy/it/u=2230509926,2741806962&fm=26&gp=0.jpg"
        },
        {
          date: "2020-08-25",
          time: "12:05:06",
          ocrResult:
            "hadfadfasdfahhfkdhjkfahdsjkafhjksdhfjkhasdfjhdsjkfhjksdahfjkhsdfjkhdjfhkjashfjkdshfjkhsdajfhsdjkfhjkhfkasdfhkjasdfkhajfkad",
          ocrImgUrl: "file:///D:/Documents/OneDrive/图片/壁纸/星树.jpg"
        }
      ],
      selectIndex: 0
    };
  },
  computed: {
    datetime(date, time) {
      return (date, time) => {
        return date + "\t" + time;
      };
    },
    simpleWord(word) {
      return (word) => {
        return word.slice(0, 10) + "...";
      };
    }
  },
  methods: {
    setting() {
      console.log("设置");
    },
    minimize() {
      ipc.send("min");
    },
    quit() {
      ipc.send("quit");
    },
    selectHistory(index) {
      this.selectIndex = index;
    },
    ocr() {
      this.minimize();
      request.get("/screenshot").then((rsp) => {
        alert(rsp);
      });
    },
    historyItem(index) {
      if (this.selectIndex === index) {
        return "history-item selected";
      } else {
        return "history-item";
      }
    }
  },
  created() {
    console.log(this);
  }
};
</script>
<style scoped>
@import './style';
</style>
