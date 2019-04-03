<?xml version="1.0" encoding="ASCII"?>
<cw:Model xmi:version="2.0" xmlns:xmi="http://www.omg.org/XMI" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:cw="http://www.example.org/cw" name="asdf">
  <machine_instance xsi:type="cw:Link" machine_representation="//@machine_representation.1" name="bbb" source="//@network.4" target="//@network_instance.0"/>
  <machine_representation initial="//@machine_representation.0/@state.1" name="Battery" machine_instance="//@network.0/@machine_instance.0 //@network.0/@machine_instance.1 //@network.2/@machine_instance.0 //@network.0/@machine_instance.2 //@network.4/@machine_instance.0">
    <state name="start"/>
    <state name="ok"/>
    <state name="fail"/>
    <transition xsi:type="cw:probabilistic" From="//@machine_representation.0/@state.0" To="//@machine_representation.0/@state.1" distribution="dd"/>
    <transition xsi:type="cw:deterministic" From="//@machine_representation.0/@state.1" To="//@machine_representation.0/@state.2"/>
    <transition xsi:type="cw:Property_Tr" From="//@machine_representation.0/@state.0" To="//@machine_representation.0/@state.2" name="456"/>
    <property_r_c>
      <property_r_abstract xsi:type="cw:Property_R" name="333"/>
    </property_r_c>
  </machine_representation>
  <machine_representation name="bbb" machine_instance="//@machine_instance.0">
    <property_r_c/>
  </machine_representation>
  <machine_representation name="ddd">
    <property_r_c/>
  </machine_representation>
  <machine_representation name="sss">
    <property_r_c/>
  </machine_representation>
  <network xsi:type="cw:Network_Representation" name="Control Center">
    <machine_instance machine_representation="//@machine_representation.0">
      <property_i_abstract xsi:type="cw:Property_I" property_r="//@machine_representation.0/@property_r_c/@property_r_abstract.0"/>
      <property_i_abstract xsi:type="cw:none" property_tr="//@machine_representation.0/@transition.2" name="456"/>
    </machine_instance>
    <machine_instance machine_representation="//@machine_representation.0">
      <property_i_abstract xsi:type="cw:Property_I" value="asdf" property_r="//@machine_representation.0/@property_r_c/@property_r_abstract.0"/>
      <property_i_abstract xsi:type="cw:probabilistic_p" property_tr="//@machine_representation.0/@transition.2" distribution="111" parameter="222"/>
    </machine_instance>
    <machine_instance machine_representation="//@machine_representation.0">
      <property_i_abstract xsi:type="cw:Property_I" property_r="//@machine_representation.0/@property_r_c/@property_r_abstract.0"/>
      <property_i_abstract xsi:type="cw:none" property_tr="//@machine_representation.0/@transition.2" name="456"/>
    </machine_instance>
  </network>
  <network xsi:type="cw:Network_Representation" name="111"/>
  <network xsi:type="cw:Network_Representation" name="222">
    <machine_instance machine_representation="//@machine_representation.0">
      <property_i_abstract xsi:type="cw:Property_I" property_r="//@machine_representation.0/@property_r_c/@property_r_abstract.0"/>
      <property_i_abstract xsi:type="cw:none" property_tr="//@machine_representation.0/@transition.2" name="456"/>
    </machine_instance>
  </network>
  <network xsi:type="cw:Network_Representation" name=",,"/>
  <network xsi:type="cw:Network_Rep_Instance" name="123">
    <machine_instance machine_representation="//@machine_representation.0" name="Battery">
      <property_i_abstract xsi:type="cw:Property_I" property_r="//@machine_representation.0/@property_r_c/@property_r_abstract.0"/>
      <property_i_abstract xsi:type="cw:none" property_tr="//@machine_representation.0/@transition.2" name="456"/>
    </machine_instance>
  </network>
  <network xsi:type="cw:Network_Rep_Instance" name="ggg"/>
  <network_instance network_representation="//@network.0" name="Control Center"/>
  <group name="Substation" groupable="//@machine_instance.0 //@network.4 //@network.5 //@network_instance.0"/>
</cw:Model>
