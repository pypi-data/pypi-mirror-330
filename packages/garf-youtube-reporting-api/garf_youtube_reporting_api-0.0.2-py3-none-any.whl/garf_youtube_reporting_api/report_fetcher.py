# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Defines report fetcher."""

from garf_core import parsers, report_fetcher
from garf_youtube_reporting_api import query_editor
from garf_youtube_reporting_api.api_clients import YouTubeReportingApiClient


class YouTubeReportingApiReportFetcher(report_fetcher.ApiReportFetcher):
  """Defines report fetcher."""

  def __init__(
    self,
    api_client: YouTubeReportingApiClient = YouTubeReportingApiClient(),
    parser: parsers.DictParser = parsers.DictParser,
    query_spec: query_editor.YouTubeReportingApiQuery = (
      query_editor.YouTubeReportingApiQuery
    ),
  ) -> None:
    """Initializes YouTubeDataApiReportFetcher."""
    super().__init__(api_client, parser, query_spec)
