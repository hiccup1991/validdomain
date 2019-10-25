import requests
import logging
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', filename='logger.info', level=logging.INFO)
def br_verify_domain(domain, api_key):
    # This call verifies if the domain is a valid website.
    try:
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        logger.info("------------------------   Initializing the domain verification routine br_verify_domain  ---------------------------------")

        try:
            # Does domain start with "http://"
            if domain[:7]== "http://" or domain[:8]== "https://":
                logger.info("about to process domain = {}" .format(domain))
            else:
                domain = "http://" + domain.strip()
                logger.info("about to process domain = {}".format(domain))
        except Exception as e:
            logger.exception("The domain prep function failed with message = {}" .format(e))


        logger.info("About to call domain with parameters = {}" .format(domain))

        try:
            # just return the header and see if a 200 code is returned.
            logger.info("About to call requests.head with domain = {}".format(domain))
            resp = requests.head(domain, headers = {'User-Agent': 'Mozilla/5.0'})
            logger.info("The requests.head returned code = {}, text = {}, headers = {}".format(resp.status_code, resp.text, resp.headers))

            if resp.status_code < 400:
                logger.info("The request domain header validated the website. ")
                return True
            else:
                primary_fail = True

        except Exception as e:
            logger.exception(("The Exception {} occured when trying to get header from website".format(e)))
            primary_fail = True

        try:
            logger.info("About to call requests.get as a stream")
            with requests.get(domain, stream=True, headers = {'User-Agent': 'Mozilla/5.0'}) as response:
                try:
                    response.raise_for_status()
                    logger.info("About to return true...")
                    return True

                except requests.exceptions.HTTPError as e:
                    logger.exception("The exception = {}".format(e))
                    # try a secondary test to verify...
                    primary_fail = True
        except requests.exceptions.ConnectionError as e:
            logger.exception("The web site verification failed - exception {} ".format(e))
            return False

        if primary_fail:
            try:
                logger.info("About to call the requests.get with domain = {}".format(domain))
                result = requests.get(domain, headers = {'User-Agent': 'Mozilla/5.0'})
                logger.info("The requests.get call returned - {}" .format(result))
                if result.status_code == 200:
                    logger.info('The second web site verification says the Web site exists')
                    return True
                else:
                    logger.info('The second web site verification says the Web site Does NOT exist Too - {}'.format(result))
                    return False
            except Exception as e:
                logger.exception("The second verify domain failed... - {}" .format(e))

    except Exception as e:
        logger.exception("The br_verify_email call failed with response = {}" .format(e))
        return False

br_verify_domain('http://mcguireandhester.com', '1')
br_verify_domain('http://www.corporatesigns.com', '1')
