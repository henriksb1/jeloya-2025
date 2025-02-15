import { BaseScene } from './BaseScene';
import { SpeedGauge } from '../Components/SpeedGauge';
import { TrackRadar } from '../Components/TrackRadar';
import { GameScene } from './GameScene';

export class RaceUiScene extends BaseScene {
	public timerText: Phaser.GameObjects.BitmapText;
	public timeLargeText: Phaser.GameObjects.BitmapText;
	public timeSmallText: Phaser.GameObjects.BitmapText;
	public speedGauge: SpeedGauge;
	public trackRadar: TrackRadar;
	public gameScene: GameScene;

	public timer: Phaser.Tweens.Tween;

	constructor(key: string, options: any) {
		super('RaceUiScene');
	}

	public create(gameScene: GameScene): void {
		this.gameScene = gameScene;
		this.timeLargeText = this.add.bitmapText(this.scale.gameSize.width / 2 + 30, 5, 'numbers', '000', 32).setOrigin(1, 0).setTint(0xffcccc);
		this.timeSmallText = this.add.bitmapText(this.scale.gameSize.width / 2 + 33, 8, 'numbers', '000', 16).setOrigin(0, 0).setTint(0xffcccc);
		this.timerText = this.add.bitmapText(this.scale.gameSize.width / 2 + 54, 8, 'impact', 'time', 16).setOrigin(0, 0);

		this.speedGauge = new SpeedGauge(this, 60, 60, 50);
		this.trackRadar = new TrackRadar(this, this.scale.gameSize.width - 40, 10);

		this.timer = this.tweens.addCounter({
			from: 180,
			to: 0,
			duration: 180000,
		});

		this.setupEvents();
	}

	public update(): void {
		const timerValue = this.timer.getValue().toFixed(2).split('.');
		this.timeLargeText.setText(timerValue[0]);
		this.timeSmallText.setText(timerValue[1]);

		this.trackRadar.update();
		const radarCars = this.gameScene.getRadarCars(700);
		for (const car of radarCars) {
			this.trackRadar.drawCar(car.offset, car.trackPosition - this.gameScene.player.trackPosition);
		}
	}

	public destroy(): void {
		this.registry.events.off('changedata');
	}

	private setupEvents(): void {
		this.registry.events.on('changedata', (parent: any, key: string, data: any) => {
			switch (key) {
				case 'speed':
					this.speedGauge.speed = data;
					break;

				case 'playerx':
					this.trackRadar.updatePlayerX(data);
					break;

				default:
					console.warn('unknown registry change');
			}
		}, this);
	}

}
