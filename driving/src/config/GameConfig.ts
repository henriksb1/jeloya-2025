import { PasuunaPlugin } from '@pinkkis/phaser-plugin-pasuuna';

// phaser game config
export const gameConfig: GameConfig = {
	type: Phaser.AUTO,
	scale: {
		parent: 'game-container',
		mode: Phaser.Scale.FIT,
		autoCenter: Phaser.Scale.CENTER_BOTH,
		// width: 320,
		// height: 180,
		width: 1280,
		height: 720,
		// width: document.querySelector('html').clientWidth,
		// height: document.querySelector('html').clientHeight,
	},
	render: {
		pixelArt: true,
	},
	plugins: {
		global: [
			{
				key: 'PasuunaPlayerPlugin',
				plugin: PasuunaPlugin,
				start: true,
				mapping: 'pasuuna',
			},
		] as any[],
	},
};
