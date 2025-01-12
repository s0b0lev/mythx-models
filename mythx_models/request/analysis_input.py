from mythx_models.request.analysis_status import AnalysisStatusRequest


class AnalysisInputRequest(AnalysisStatusRequest):
    @property
    def endpoint(self):
        """The API's analysis request input endpoint.

        :return: A string denoting the request input endpoint without the host prefix
        """
        return "v1/analyses/{}/input".format(self.uuid)
