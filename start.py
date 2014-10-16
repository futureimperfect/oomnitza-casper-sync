"""
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import os

from models.casper_connection import CasperConnection
from models.oomnitza_connection import OomnitzaConnection

# initialize service wrappers
casper = CasperConnection(os.path.join(os.path.abspath(os.path.join(__file__, os.pardir)), "config.ini"))
oomnitza = OomnitzaConnection(os.path.join(os.path.abspath(os.path.join(__file__, os.pardir)), "config.ini"))


def main():
    """
    Main entry point for Oomnitza & Casper synchronization
    """
    # perform synchronization
    print "Oomnitza Casper Synchronization\n[x] Sync has started..."
    oomnitza.sync_assets(casper.get_the_details_of_all_the_computers())
    print "[x] Sync has completed. Bye!"
    return True


if __name__ == '__main__':
    main()
