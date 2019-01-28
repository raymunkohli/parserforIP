<?xml version="1.0" encoding="ASCII"?>
<cw:Model xmi:version="2.0" xmlns:xmi="http://www.omg.org/XMI" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:cw="http://www.example.org/cw" name="length">
  <machine initial="//@machine.0/@state.0" name="Batteryy" type="state-machine">
    <state name="ok"/>
    <state name="fail"/>
    <transition xsi:type="cw:probabilistic" to="//@machine.0/@state.1" from="//@machine.0/@state.0" parameter="13.3" distribution="exponential"/>
    <transition xsi:type="cw:probabilistic" to="//@machine.0/@state.0" from="//@machine.0/@state.1" parameter="333.0" distribution="exponential"/>
    <property name="Capisity" value="103" type="Number"/>
  </machine>
  <machine xsi:type="cw:Link" name="sub123-sub101-0" type="state-machine" target="//@network.1/@represented" source="//@network.0/@represented">
    <property name="kv" value="state-machine" type="string"/>
    <property name="x" type="number"/>
    <property name="max" type="number"/>
    <property name="overloaded" type="boolean"/>
    <property name="connected" type="boolean"/>
    <property name="length" type="number"/>
  </machine>
  <network>
    <machine initial="//@network.0/@machine.0/@state.0" name="Battery" type="state-machine">
      <state name="ok"/>
      <state name="fail"/>
      <transition xsi:type="cw:probabilistic" to="//@network.0/@machine.0/@state.1" from="//@network.0/@machine.0/@state.0" parameter="13.3" distribution="exponential"/>
      <transition xsi:type="cw:probabilistic" to="//@network.0/@machine.0/@state.0" from="//@network.0/@machine.0/@state.1" parameter="333.0" distribution="exponential"/>
      <property name="Capisity" value="103" type="Number"/>
    </machine>
    <represented initial="//@network.0/@represented/@state.0" name="sub123" type="state-machine">
      <state name="ok"/>
      <state name="fail"/>
      <transition xsi:type="cw:probabilistic" to="//@network.0/@represented/@state.0" from="//@network.0/@represented/@state.1" parameter="0.1" distribution="exponential"/>
      <transition xsi:type="cw:probabilistic" to="//@network.0/@represented/@state.1" from="//@network.0/@represented/@state.0" parameter="20.0" distribution="exponential"/>
      <property name="Load" value="123" type="Number"/>
    </represented>
    <network super="//@network.0">
      <machine initial="//@network.0/@network.0/@machine.0/@state.0" name="Battery" type="state-machine">
        <state name="ok"/>
        <state name="fail"/>
        <transition xsi:type="cw:probabilistic" to="//@network.0/@network.0/@machine.0/@state.1" from="//@network.0/@network.0/@machine.0/@state.0" parameter="13.3" distribution="exponential"/>
        <transition xsi:type="cw:probabilistic" to="//@network.0/@network.0/@machine.0/@state.0" from="//@network.0/@network.0/@machine.0/@state.1" parameter="333.0" distribution="exponential"/>
        <property name="Capisity" value="103" type="Number"/>
      </machine>
      <represented name="New Network" type="network-machine" parent="//@network.0"/>
    </network>
  </network>
  <network>
    <machine initial="//@network.1/@machine.0/@state.0" name="Battery" type="state-machine">
      <state name="ok"/>
      <state name="fail"/>
      <transition xsi:type="cw:probabilistic" to="//@network.1/@machine.0/@state.1" from="//@network.1/@machine.0/@state.0" parameter="13.3" distribution="exponential"/>
      <transition xsi:type="cw:probabilistic" to="//@network.1/@machine.0/@state.0" from="//@network.1/@machine.0/@state.1" parameter="333.0" distribution="exponential"/>
      <property name="Capisity" value="103" type="Number"/>
    </machine>
    <represented initial="//@network.1/@represented/@state.0" name="sub101" type="state-machine">
      <state name="ok"/>
      <state name="fail"/>
      <transition xsi:type="cw:probabilistic" to="//@network.1/@represented/@state.0" from="//@network.1/@represented/@state.1" parameter="0.1" distribution="exponential"/>
      <transition xsi:type="cw:probabilistic" to="//@network.1/@represented/@state.1" from="//@network.1/@represented/@state.0" parameter="20.0" distribution="exponential"/>
      <property name="Load" value="333" type="Number"/>
    </represented>
  </network>
  <network>
    <represented initial="//@network.2/@represented/@state.0" name="sub101" type="state-machine">
      <state name="ok"/>
      <state name="fail"/>
      <transition xsi:type="cw:probabilistic" to="//@network.2/@represented/@state.0" from="//@network.2/@represented/@state.1" parameter="0.1" distribution="exponential"/>
      <transition xsi:type="cw:probabilistic" to="//@network.2/@represented/@state.1" from="//@network.2/@represented/@state.0" parameter="20.0" distribution="exponential"/>
      <property name="Load" value="222" type="Number"/>
    </represented>
  </network>
</cw:Model>
