const { SlippiGame } = require("@slippi/slippi-js");
const fs = require('fs');

// console.log(stats);//console.log(stats.stocks);//console.log(stats.conversions);//console.log(stats.combos);// console.log(frames[0].players); // console.log(settings.players);// console.log(metadata.players);//console.log(stats.actionCounts);//console.log(metadata.players);

let input_folder = 'C:/Users/cjsch/Documents/Slippi/old/'
//let file = "Game_20221101T165807.slp"
//let full_filename = input_folder + file

//let file_sub = "Game_20221101T165807"
let output_folder = 'json/'

let directoryPath = input_folder
fs.readdir(directoryPath, function (err, files) {
  //handling error
  if (err) {
      return console.log('Unable to scan directory: ' + err);
  } 
  //listing all files using forEach
  files.forEach(function (file) {
      // Do whatever you want to do with the file
      //console.log(file); 
      let file_sub = file.substring(0,20)
      const game = new SlippiGame(input_folder + file);
      const settings = game.getSettings();
      const metadata = game.getMetadata();
      const stats = game.getStats();
      // console.log(stats['overall']);
      let new_json = {'settings': settings,'metadata':metadata,'stats':stats};
      let stats_string = JSON.stringify(new_json, null, 4);
      fs.writeFileSync(output_folder + file_sub + '.json', stats_string, err => {
          if (err) {
            console.error(err);
          }
          // file written successfully
        });

  });
});

