"""Custom topology example

Two directly connected switches plus a host for each switch:

   host --- switch --- switch --- host

Adding the 'topos' dict with a key/value pair to generate our newly defined
topology enables one to pass in '--topo=mytopo' from the command line.
"""

from mininet.topo import Topo

class MyTopo( Topo ):
    "Simple topology example."

    def __init__( self ):
        "Create custom topo."

        # Initialize topology
        Topo.__init__( self )

        # Add hosts and switches
        leftHost = self.addHost( 'h1' )
        rightHost = self.addHost( 'h4' )
        leftHost2 = self.addHost( 'h2' )
	upHost = self.addHost( 'h3' )
	downHost = self.addHost( 'h5' )	
        leftSwitch = self.addSwitch( 's1' )
        rightSwitch = self.addSwitch( 's3' )
        upSwitch = self.addSwitch( 's2' )
        downSwitch = self.addSwitch( 's4' )
	# Add links
        self.addLink( leftHost, leftSwitch )
	self.addLink( leftHost2, leftSwitch )
	self.addLink( upHost, upSwitch )
	self.addLink( rightHost, rightSwitch )
	self.addLink( downHost, rightSwitch )
        self.addLink( leftSwitch, upSwitch, bw=10 )
        self.addLink( leftSwitch, downSwitch, bw=5 )
	self.addLink( rightSwitch, upSwitch, bw=20 )
	self.addLink( rightSwitch, downSwitch, bw=10 )
	self.addLink( upSwitch, downSwitch, bw=10 )

topos = { 'mytopo': ( lambda: MyTopo() ) }
