import './libs/GLTFLoader';
import 'phaser';
import '@csstools/normalize.css';
import './css/styles.css';
import { BootScene } from './scenes/BootScene';
import { gameConfig } from './config/GameConfig';
import { LoadScene } from './scenes/LoadScene';
import { GameScene } from './scenes/GameScene';
import { RaceUiScene } from './scenes/RaceUiScene';

// set up game class, and global stuff
export class PoisonVialGame extends Phaser.Game {
	private debug: boolean = false;

	constructor(config: GameConfig) {
		super(config);
	}
}

// start the game
window.onload = () => {
	const socket = new WebSocket('ws://10.168.74.112:8765');

	socket.onopen = (event) => {
		console.log("Here's some text that the server is urgently awaiting!");
	  };
	  


	const game = new PoisonVialGame(gameConfig);

	// set up stats
	if (window.env.buildType !== 'production') {
		const Stats = require('stats-js');
		const stats = new Stats();
		stats.setMode(0); // 0: fps, 1: ms
		stats.domElement.style.position = 'absolute';
		stats.domElement.style.left = '0px';
		stats.domElement.style.top = '0px';
		document.body.appendChild(stats.domElement);

		game.events.on('prestep', () => stats.begin());
		game.events.on('postrender', () => stats.end());
	}

	game.scene.add('BootScene', BootScene, true);
	game.scene.add('LoadScene', LoadScene, false);
	game.scene.add('GameScene', GameScene, false);
	game.scene.add('RaceUiScene', RaceUiScene, false);
};
