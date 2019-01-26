<?xml version="1.0" encoding="ASCII"?>
<cw:Model xmi:version="2.0" xmlns:xmi="http://www.omg.org/XMI" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:cw="http://www.example.org/cw" name="length">
  <machine xsi:type="cw:Link" target="//@network.1/@represented" source="//@network.0/@represented">
    <property name="kv" value="state-machine" type="string"/>
    <property name="x" type="number"/>
    <property name="max" type="number"/>
    <property name="overloaded" type="boolean"/>
    <property name="connected" type="boolean"/>
    <property name="length" type="number"/>
  </machine>
  <machine initial="//@machine.1/@state.0" name="Battery" type="state-machine">
    <state name="ok"/>
    <state name="fail"/>
    <transition xsi:type="cw:probabilistic" to="//@machine.1/@state.1" from="//@machine.1/@state.0" parameter="0.1" distribution="exponential"/>
    <transition xsi:type="cw:probabilistic" to="//@machine.1/@state.1" from="//@machine.1/@state.0" parameter="20.0"/>
  </machine>
  <network>
    <machine name="mamamia" parent="//@network.0"/>
    <represented initial="//@network.0/@represented/@state.0" name="123">
      <state name="ok"/>
      <state name="fail"/>
      <transition xsi:type="cw:probabilistic" to="//@network.0/@represented/@state.0" from="//@network.0/@represented/@state.1" parameter="0.1" distribution="exponential"/>
      <transition xsi:type="cw:probabilistic" to="//@network.0/@represented/@state.1" from="//@network.0/@represented/@state.0" parameter="20.0" distribution="exponential"/>
      <property name="Load"/>
    </represented>
    <network super="//@network.0">
      <represented name="123123" type="network-machine" parent="//@network.0"/>
    </network>
  </network>
  <network>
    <represented initial="//@network.1/@represented/@state.0" name="333">
      <state name="ok"/>
      <state name="fail"/>
      <transition xsi:type="cw:probabilistic" to="//@network.1/@represented/@state.0" from="//@network.1/@represented/@state.1" parameter="0.1" distribution="exponential"/>
      <transition xsi:type="cw:probabilistic" to="//@network.1/@represented/@state.1" from="//@network.1/@represented/@state.0" parameter="20.0" distribution="exponential"/>
      <property name="Load" value="123" type="Number"/>
    </represented>
    <network super="//@network.1">
      <represented name="Relay" parent="//@network.1">
        <property/>
      </represented>
    </network>
  </network>
</cw:Model>
