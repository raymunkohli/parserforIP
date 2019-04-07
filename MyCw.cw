<?xml version="1.0" encoding="ASCII"?>
<cw:Model xmi:version="2.0" xmlns:xmi="http://www.omg.org/XMI" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:cw="http://www.example.org/cw" name="asdf">
  <machine_instance machine_representation="//@machine_representation.0" name="aaa">
    <property_i_abstract xsi:type="cw:Property_I" property_r="//@machine_representation.0/@property_r_c/@property_r_abstract.0"/>
    <property_i_abstract xsi:type="cw:none" property_tr="//@machine_representation.0/@transition.1" name="hjkl"/>
    <property_i_abstract xsi:type="cw:Property_I" property_r="//@machine_representation.0/@property_r_c/@property_r_abstract.1"/>
  </machine_instance>
  <machine_instance machine_representation="//@machine_representation.0" name="aaa">
    <property_i_abstract xsi:type="cw:Property_I" property_r="//@machine_representation.0/@property_r_c/@property_r_abstract.0"/>
    <property_i_abstract xsi:type="cw:none" property_tr="//@machine_representation.0/@transition.1" name="hjkl"/>
    <property_i_abstract xsi:type="cw:Property_I" property_r="//@machine_representation.0/@property_r_c/@property_r_abstract.1"/>
  </machine_instance>
  <machine_instance xsi:type="cw:Link" machine_representation="//@machine_representation.1" name="aaa-asdf-1" source="//@machine_instance.0" target="//@network.1">
    <property_i_abstract xsi:type="cw:Property_I" value="12131" property_r="//@machine_representation.1/@property_r_c/@property_r_abstract.0"/>
    <property_i_abstract xsi:type="cw:deterministic_p" property_tr="//@machine_representation.1/@transition.0" name="sdae"/>
  </machine_instance>
  <machine_representation initial="//@machine_representation.0/@state.0" name="aaa" instance="//@network.1/@machine_instance.0 //@machine_instance.0 //@machine_instance.1 //@network.0/@machine_instance.0">
    <state name="ok"/>
    <state name="fail"/>
    <transition xsi:type="cw:probabilistic" From="//@machine_representation.0/@state.0" To="//@machine_representation.0/@state.1"/>
    <transition xsi:type="cw:Property_Tr" From="//@machine_representation.0/@state.1" To="//@machine_representation.0/@state.0" name="hjkl"/>
    <property_r_c>
      <property_r_abstract xsi:type="cw:Property_R" name="123"/>
      <property_r_abstract xsi:type="cw:Property_R" name="aaa"/>
    </property_r_c>
  </machine_representation>
  <machine_representation initial="//@machine_representation.1/@state.0" name="link" instance="//@machine_instance.2">
    <state name="ok"/>
    <state name="fail"/>
    <transition xsi:type="cw:Property_Tr" From="//@machine_representation.1/@state.0" To="//@machine_representation.1/@state.1" name="sdae"/>
    <property_r_c>
      <property_r_abstract xsi:type="cw:Property_R" name="aaa"/>
    </property_r_c>
  </machine_representation>
  <network xsi:type="cw:Network_Representation" name="sadwfawdd" instance="//@network_instance.0 //@network.1/@network_instance.0">
    <machine_instance machine_representation="//@machine_representation.0" name="aaa">
      <property_i_abstract xsi:type="cw:Property_I" property_r="//@machine_representation.0/@property_r_c/@property_r_abstract.0"/>
      <property_i_abstract xsi:type="cw:none" property_tr="//@machine_representation.0/@transition.1" name="hjkl"/>
      <property_i_abstract xsi:type="cw:Property_I" property_r="//@machine_representation.0/@property_r_c/@property_r_abstract.1"/>
    </machine_instance>
    <property_r_c>
      <property_r_abstract xsi:type="cw:Property_R" name="hjk">
        <nestedproperty name="yui" value="21345"/>
      </property_r_abstract>
      <property_r_abstract xsi:type="cw:Property_R" name="ghjk"/>
    </property_r_c>
  </network>
  <network xsi:type="cw:Network_Rep_Instance" name="asdf">
    <machine_instance machine_representation="//@machine_representation.0" name="aaa">
      <property_i_abstract xsi:type="cw:Property_I" property_r="//@machine_representation.0/@property_r_c/@property_r_abstract.0"/>
      <property_i_abstract xsi:type="cw:none" property_tr="//@machine_representation.0/@transition.1" name="hjkl"/>
      <property_i_abstract xsi:type="cw:Property_I" property_r="//@machine_representation.0/@property_r_c/@property_r_abstract.1"/>
    </machine_instance>
    <property_r_c>
      <property_r_abstract xsi:type="cw:propertyFull" name="ghj"/>
    </property_r_c>
    <network_instance network_representation="//@network.0" name="sadwfawdd">
      <property_i_abstract xsi:type="cw:Property_I" property_r="//@network.0/@property_r_c/@property_r_abstract.0"/>
      <property_i_abstract xsi:type="cw:Property_I" property_r="//@network.0/@property_r_c/@property_r_abstract.1"/>
    </network_instance>
  </network>
  <network xsi:type="cw:Network_Rep_Instance" name="dfghj">
    <property_r_c/>
  </network>
  <network_instance network_representation="//@network.0" name="sadwfawd">
    <property_i_abstract xsi:type="cw:Property_I" value="6789" property_r="//@network.0/@property_r_c/@property_r_abstract.0"/>
    <property_i_abstract xsi:type="cw:Property_I" value="789" property_r="//@network.0/@property_r_c/@property_r_abstract.1"/>
  </network_instance>
</cw:Model>
