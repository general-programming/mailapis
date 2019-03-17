import txt from './test_mail.txt';

const loadMail = (mailID) => {
	if (mailID === 'testmail') {
		return txt;
	}
};

export default loadMail;