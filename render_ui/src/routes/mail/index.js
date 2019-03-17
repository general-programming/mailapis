import { h, Component } from 'preact';
// import { simpleParser } from 'mailparser';

import style from './style';
import loadMail from './loader';

export default class Profile extends Component {
	state = {
		time: Date.now()
	};

	// update the current time
	updateTime = () => {
		this.setState({ time: Date.now() });
	};

	// gets called when this route is navigated to
	componentDidMount() {
		// start a timer for the clock:
		// this.timer = setInterval(this.updateTime, 1000);
	}

	// gets called just before navigating away from the route
	componentWillUnmount() {
		// clearInterval(this.timer);
	}

	// Note: `user` comes from the URL, courtesy of our router
	render({ mail }, { time }) {
		return (
			<div class={style.mail}>
				<h1>Mail: {mail}</h1>
                <p>{loadMail('testmail')}</p>
			</div>
		);
	}
}