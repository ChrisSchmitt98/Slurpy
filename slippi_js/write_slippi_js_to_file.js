const { SlippiGame } = require("@slippi/slippi-js");
const fs = require('fs');
const Chart = require('chart.js');

class SlippiActionCounts {
  constructor(actionCounts, playerID) {
      this.airDodge = actionCounts[playerID]["airDodgeCount"];
      this.dashDance = actionCounts[playerID]["dashDanceCount"];
      this.grabFail = actionCounts[playerID]["grabCount"]['fail'];
      this.grabSuccess = actionCounts[playerID]["grabCount"]['success'];
      this.groundTechAway = actionCounts[playerID]["groundTechCount"]['away'];
      this.groundTechIn = actionCounts[playerID]["groundTechCount"]['in'];
      this.groundTechNeutral = actionCounts[playerID]["groundTechCount"]['neutral'];
      this.groundTechFail = actionCounts[playerID]["groundTechCount"]['fail'];
      this.bair = actionCounts[playerID]["attackCount"]["bair"];
      this.dair = actionCounts[playerID]["attackCount"]["dair"];
      this.dash = actionCounts[playerID]["attackCount"]["dash"];
      this.dsmash = actionCounts[playerID]["attackCount"]["dsmash"];
      this.dtilt = actionCounts[playerID]["attackCount"]["dtilt"];
      this.fair = actionCounts[playerID]["attackCount"]["fair"];
      this.fsmash = actionCounts[playerID]["attackCount"]["fsmash"];
      this.ftilt = actionCounts[playerID]["attackCount"]["ftilt"];
      this.jab1 = actionCounts[playerID]["attackCount"]["jab1"];
      this.jab2 = actionCounts[playerID]["attackCount"]["jab2"];
      this.jab3 = actionCounts[playerID]["attackCount"]["jab3"];
      this.jabm = actionCounts[playerID]["attackCount"]["jabm"];
      this.nair = actionCounts[playerID]["attackCount"]["nair"];
      this.uair = actionCounts[playerID]["attackCount"]["uair"];
      this.usmash = actionCounts[playerID]["attackCount"]["usmash"];
      this.utilt = actionCounts[playerID]["attackCount"]["utilt"];
  }
}
class SlippiMeta {
  constructor(metadata, playerID) {
      this.netplay = metadata["players"][playerID]["names"]["netplay"];
      this.code = metadata["players"][playerID]["names"]["code"];

  }
}

// as a prototype this is harded coded for my local hardrive, but the end prodcut should be pulling the .slp info from an sql database ideally

let input_folder = 'C:/Users/Ryan/Documents/Slippi Files/'
//let output_folder = 'json/'
//let directoryPath = input_folder

function getData(input_folder) {
  fs.readdir(input_folder, function (err, files) {
    data = {};
    //handling error
    if (err) {
        console.log('Unable to scan directory: ' + err);
    }
    let str1 = "Reading .slp files from ";
    console.log(str1.concat(input_folder));
    //listing all files using forEach
    files.forEach(function (file) {
        let file_sub = file.substring(0,20);
        const game = new SlippiGame(input_folder + file);
        const settings = game.getSettings();
        const metadata = game.getMetadata();
        const stats = game.getStats();
        data[file_sub] = {"Settings": settings ,"Metadata": metadata , "Stats": stats};
    })
    console.log(data)
    dummy_GameID = "Game_20221201T132125";
    const player1Counts = new SlippiActionCounts(data[dummy_GameID]["Stats"]["actionCounts"], 0);
    const player2Counts = new SlippiActionCounts(data[dummy_GameID]["Stats"]["actionCounts"], 1);
    const player1Meta = new SlippiMeta(data[dummy_GameID]["Metadata"], 0)
    const player2Meta = new SlippiMeta(data[dummy_GameID]["Metadata"], 1)
    new Chart("myChart", {
      type: "bar",
      data: {
        labels: [player1Meta.netplay, player2Meta.netplay],
        datasets: [{
          backgroundColor:["red", "blue"],
          data: [player1Counts.grabSuccess, player2Counts.grabSuccess]
        }]
      },
      options: {}
    }
    )
  }) 
}

var data = getData(input_folder)

// we now have dictionaries of each game and it's data (this would ideally be done at backend through SQL.) Lets access the data based on USer request
// which would be done in the website by clicking ona  certain game, and plot data assciated with that gameID. I'm going to nest the dictionaries for this, 
// but functionally this should be the same as calling from  SQL database
//function processData(data) {
//  
//  const player1Counts = new SlippiActionCounts(data[dummy_GameID], 0);
//  const player2Counts = new SlippiActionCounts(data[dummy_GameID], 1);
//}


