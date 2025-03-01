from pysll.models import Function


# ------------------------------------ Manually defined operations -------------------------------------
class RoboticSamplePreparation(Function):
    """A wrapper that can be used to explicitly specify robotic execution of
    subsets of operations within a list of ExperimentSamplePreparation Unit
    Operations.

    The allowed input signatures of RoboticSamplePreparation is:

    ```RoboticSamplePreparation(UnitOperations)``` creates a `Protocol` object that will perform the robotic sample
    preparation specified in `UnitOperations`.

    :param `UnitOperations`: "The unit operations that specify how to perform the sample preparation.
    :returns: None - This is simply an inert head that is meant to separate manual and robotic preparation steps.

    All available unit operations can be found in the 'Experimental Principles' section of the site: https://www.emeraldcloudlab.com/helpfiles/experimentroboticsamplepreparation.
    """


class ManualSamplePreparation(Function):
    """A wrapper that can be used to explicitly specify manual execution of
    subsets of operations within a list of ExperimentSamplePreparation Unit
    Operations.

    The allowed input signatures of RoboticSamplePreparation is:

    ```ManualSamplePreparation(UnitOperations)``` creates a `Protocol` object that will perform the manual sample
    preparation specified in `UnitOperations`.

    :param `UnitOperations`: "The unit operations that specify how to perform the sample preparation.
    :returns: None - This is simply an inert head that is meant to separate manual and robotic preparation steps.

    All available unit operations can be found in the 'Experimental Principles' section of the site: https://www.emeraldcloudlab.com/helpfiles/experimentmanualsamplepreparation.
    """


# --------------------------- Automatically defined operations (paste below) ---------------------------
class AbsorbanceIntensity(Function):
    """The allowed input signatures of AbsorbanceIntensity without optional
    arguments (kwargs) are:

    ``AbsorbanceIntensity(Options, **kwargs)`` measures the absorbance intensity data of the input samples.

    :param `**kwargs`: optional arguments for AbsorbanceIntensity.
    :returns: UnitOperation - The unit operation that is to be used in sample/cell preparation.

    All optional parameters (kwargs) can be found in the 'Options' tab of the site: https://www.emeraldcloudlab.com/helpfiles/absorbanceintensity.
    """


class AbsorbanceKinetics(Function):
    """The allowed input signatures of AbsorbanceKinetics without optional
    arguments (kwargs) are:

    ``AbsorbanceKinetics(Options, **kwargs)`` measures the absorbance kinetics data of the input samples.

    :param `**kwargs`: optional arguments for AbsorbanceKinetics.
    :returns: UnitOperation - The unit operation that is to be used in sample/cell preparation.

    All optional parameters (kwargs) can be found in the 'Options' tab of the site: https://www.emeraldcloudlab.com/helpfiles/absorbancekinetics.
    """


class AbsorbanceSpectroscopy(Function):
    """The allowed input signatures of AbsorbanceSpectroscopy without optional
    arguments (kwargs) are:

    ``AbsorbanceSpectroscopy(Options, **kwargs)`` measures the absorbance spectroscopy data of the input samples.

    :param `**kwargs`: optional arguments for AbsorbanceSpectroscopy.
    :returns: UnitOperation - The unit operation that is to be used in sample/cell preparation.

    All optional parameters (kwargs) can be found in the 'Options' tab of the site: https://www.emeraldcloudlab.com/helpfiles/absorbancespectroscopy.
    """


class AdjustpH(Function):
    """The allowed input signatures of AdjustpH without optional arguments
    (kwargs) are:

    ``AdjustpH(Options, **kwargs)`` adjusts the pHs of the given samples to the specified nominal pHs by adding acid and/or base.

    :param `**kwargs`: optional arguments for AdjustpH.
    :returns: UnitOperation - The unit operation that is to be used in sample/cell preparation.

    All optional parameters (kwargs) can be found in the 'Options' tab of the site: https://www.emeraldcloudlab.com/helpfiles/adjustph.
    """


class Aliquot(Function):
    """The allowed input signatures of Aliquot without optional arguments
    (kwargs) are:

    ``Aliquot(aliquotRules, **kwargs)`` generates an ExperimentSampleManipulation-compatible 'primitive' that describes aliquoting of a single source to multiple destinations.

    :param `**kwargs`: optional arguments for Aliquot.
    :returns: None

    All optional parameters (kwargs) can be found in the 'Options' tab of the site: https://www.emeraldcloudlab.com/helpfiles/aliquot.
    """


class AlphaScreen(Function):
    """The allowed input signatures of AlphaScreen without optional arguments
    (kwargs) are:

    ``AlphaScreen(Options, **kwargs)`` measures the alpha screen data of the input samples.

    :param `**kwargs`: optional arguments for AlphaScreen.
    :returns: UnitOperation - The unit operation that is to be used in sample/cell preparation.

    All optional parameters (kwargs) can be found in the 'Options' tab of the site: https://www.emeraldcloudlab.com/helpfiles/alphascreen.
    """


class Centrifuge(Function):
    """The allowed input signatures of Centrifuge without optional arguments
    (kwargs) are:

    ``Centrifuge(centrifugeRules, **kwargs)`` generates an ExperimentSampleManipulation-compatible 'primitive' that describes centrifuging a sample at a specified intensity for a specified amount of time.

    :param `**kwargs`: optional arguments for Centrifuge.
    :returns: None

    All optional parameters (kwargs) can be found in the 'Options' tab of the site: https://www.emeraldcloudlab.com/helpfiles/centrifuge.
    """


class ChangeMedia(Function):
    """The allowed input signatures of ChangeMedia without optional arguments
    (kwargs) are:

    ``ChangeMedia(changeMediaRules, **kwargs)`` generates an ExperimentRoboticCellPreparation-compatible 'primitive' that describes a change media process.

    :param `**kwargs`: optional arguments for ChangeMedia.
    :returns: None

    All optional parameters (kwargs) can be found in the 'Options' tab of the site: https://www.emeraldcloudlab.com/helpfiles/changemedia.
    """


class CountLiquidParticles(Function):
    """The allowed input signatures of CountLiquidParticles without optional
    arguments (kwargs) are:

    ``CountLiquidParticles(Options, **kwargs)`` generates an ExperimentSamplePreparation-compatible 'UnitOperation' that run a high accuracy light obscuration (HIAC) experiment to count liquid particles of different sizes.

    :param `**kwargs`: optional arguments for CountLiquidParticles.
    :returns: UnitOperation - The unit operation that represents this measurement.

    All optional parameters (kwargs) can be found in the 'Options' tab of the site: https://www.emeraldcloudlab.com/helpfiles/countliquidparticles.
    """


class Cover(Function):
    """The allowed input signatures of Cover without optional arguments
    (kwargs) are:

    ``Cover(Sample, **kwargs)`` generates an ExperimentSampleManipulation-compatible 'primitive' that describes placing a lid onto a plate.

    :param `**kwargs`: optional arguments for Cover.
    :returns: None

    All optional parameters (kwargs) can be found in the 'Options' tab of the site: https://www.emeraldcloudlab.com/helpfiles/cover.
    """


class CrossFlowFiltration(Function):
    """The allowed input signatures of CrossFlowFiltration without optional
    arguments (kwargs) are:

    ``CrossFlowFiltration(Options, **kwargs)`` generates an ExperimentSamplePreparation-compatible 'UnitOperation' that filter the provided sample by flowing it parallel-wise to the membrane surface.

    :param `**kwargs`: optional arguments for CrossFlowFiltration.
    :returns: UnitOperation - The unit operation that represents this measurement.

    All optional parameters (kwargs) can be found in the 'Options' tab of the site: https://www.emeraldcloudlab.com/helpfiles/crossflowfiltration.
    """


class Degas(Function):
    """The allowed input signatures of Degas without optional arguments
    (kwargs) are:

    ``Degas(Options, **kwargs)`` remove dissolved gases from the samples.

    :param `**kwargs`: optional arguments for Degas.
    :returns: UnitOperation - The unit operation that is to be used in sample/cell preparation.

    All optional parameters (kwargs) can be found in the 'Options' tab of the site: https://www.emeraldcloudlab.com/helpfiles/degas.
    """


class Dilute(Function):
    """The allowed input signatures of Dilute without optional arguments
    (kwargs) are:

    ``Dilute(Options, **kwargs)`` transfers an amount of sample into a container and dilutes it with buffers as specified.

    :param `**kwargs`: optional arguments for Dilute.
    :returns: UnitOperation - The unit operation that is to be used in sample/cell preparation.

    All optional parameters (kwargs) can be found in the 'Options' tab of the site: https://www.emeraldcloudlab.com/helpfiles/dilute.
    """


class DynamicLightScattering(Function):
    """The allowed input signatures of DynamicLightScattering without optional
    arguments (kwargs) are:

    ``DynamicLightScattering(Options, **kwargs)`` determine the hydrodynamic radius of an analyte via Dynamic Light Scattering.

    :param `**kwargs`: optional arguments for DynamicLightScattering.
    :returns: UnitOperation - The unit operation that is to be used in sample/cell preparation.

    All optional parameters (kwargs) can be found in the 'Options' tab of the site: https://www.emeraldcloudlab.com/helpfiles/dynamiclightscattering.
    """


class ExtractPlasmidDNA(Function):
    """The allowed input signatures of ExtractPlasmidDNA without optional
    arguments (kwargs) are:

    ``ExtractPlasmidDNA(Options, **kwargs)`` isolates plasmid DNA from live cell or cell lysate through lysing (if dealing with cells, rather than lysate), then neutralizing the pH of the solution to keep plasmid DNA soluble (through renaturing) and pelleting out insoluble cell components, followed by one or more rounds of optional purification techniques including  precipitation (such as a cold ethanol or isopropanol wash), liquid-liquid extraction (such as phenol:chloroform extraction), solid phase extraction (such as spin columns), and magnetic bead separation (selectively binding plasmid DNA to magnetic beads while washing non-binding impurities from the mixture).

    :param `**kwargs`: optional arguments for ExtractPlasmidDNA.
    :returns: UnitOperation - The unit operation that is to be used in sample/cell preparation.

    All optional parameters (kwargs) can be found in the 'Options' tab of the site: https://www.emeraldcloudlab.com/helpfiles/extractplasmiddna.
    """


class ExtractProtein(Function):
    """The allowed input signatures of ExtractProtein without optional
    arguments (kwargs) are:

    ``ExtractProtein(Options, **kwargs)`` isolates protein from live cell or cell lysate through lysing (if dealing with cells, rather than lysate), followed by one or more rounds of optional purification techniques including  precipitation (such as by adding ammonium sulfate, TCA (trichloroacetic acid), or acetone etc.), liquid-liquid extraction (e.g. adding C4 and C5 alcohols (butanol, pentanol) followed by ammonium sulfate into the protein-containing aqueous solution), solid phase extraction (such as spin columns), and magnetic bead separation (selectively binding proteins to magnetic beads while washing non-binding impurities from the mixture). Note that ExperimentExtractProtein is intended to extract specific or non-specific proteins from the whole cells or cell lysate.

    :param `**kwargs`: optional arguments for ExtractProtein.
    :returns: UnitOperation - The unit operation that is to be used in sample/cell preparation.

    All optional parameters (kwargs) can be found in the 'Options' tab of the site: https://www.emeraldcloudlab.com/helpfiles/extractprotein.
    """


class ExtractRNA(Function):
    """The allowed input signatures of ExtractRNA without optional arguments
    (kwargs) are:

    ``ExtractRNA(Options, **kwargs)`` isolates RNA from live cell or cell lysate samples through lysing (if the input sample contains cells, rather than lysate), clearing the lysate of cellular debris by homogenization (optional), followed by one or more rounds of optional crude purification techniques including precipitation (such as a cold ethanol or isopropanol wash), liquid-liquid extraction (such as a phenol-chloroform extraction), solid phase extraction (such as a spin column), and magnetic bead separation (selectively binding RNA to magnetic beads while washing non-binding impurities from the mixture). Digestion enzymes can be added during any of these purification steps to degrade DNA in order to improve the purity of the extracted RNA. Extracted RNA can be further purified and analyzed with experiments including, but not limited to, ExperimentHPLC, ExperimentFPLC, and ExperimentPAGE (see experiment help files to learn more).

    :param `**kwargs`: optional arguments for ExtractRNA.
    :returns: UnitOperation - The unit operation that is to be used in sample/cell preparation.

    All optional parameters (kwargs) can be found in the 'Options' tab of the site: https://www.emeraldcloudlab.com/helpfiles/extractrna.
    """


class FillToVolume(Function):
    """The allowed input signatures of FillToVolume without optional arguments
    (kwargs) are:

    ``FillToVolume(fillToVolumeRules, **kwargs)`` generates an ExperimentSampleManipulation-compatible 'primitive' that describes transfering a source into a destination until a desired volume is reached.

    :param `**kwargs`: optional arguments for FillToVolume.
    :returns: None

    All optional parameters (kwargs) can be found in the 'Options' tab of the site: https://www.emeraldcloudlab.com/helpfiles/filltovolume.
    """


class Filter(Function):
    """The allowed input signatures of Filter without optional arguments
    (kwargs) are:

    ``Filter(Sample, **kwargs)`` generates an ExperimentSampleManipulation-compatible 'primitive' that describes filtering a sample through a specified filter by applying a specified pressure for a specified amount of time.

    :param `**kwargs`: optional arguments for Filter.
    :returns: None

    All optional parameters (kwargs) can be found in the 'Options' tab of the site: https://www.emeraldcloudlab.com/helpfiles/filter.
    """


class FlashChromatography(Function):
    """The allowed input signatures of FlashChromatography without optional
    arguments (kwargs) are:

    ``FlashChromatography(Options, **kwargs)`` separate a sample via flash chromatography by flowing it through a column to which compounds in the sample will differentially adsorb.

    :param `**kwargs`: optional arguments for FlashChromatography.
    :returns: UnitOperation - The unit operation that is to be used in sample/cell preparation.

    All optional parameters (kwargs) can be found in the 'Options' tab of the site: https://www.emeraldcloudlab.com/helpfiles/flashchromatography.
    """


class FlowCytometry(Function):
    """The allowed input signatures of FlowCytometry without optional arguments
    (kwargs) are:

    ``FlowCytometry(Options, **kwargs)`` flows a sample through a flow cytometer.

    :param `**kwargs`: optional arguments for FlowCytometry.
    :returns: UnitOperation - The unit operation that is to be used in sample/cell preparation.

    All optional parameters (kwargs) can be found in the 'Options' tab of the site: https://www.emeraldcloudlab.com/helpfiles/flowcytometry.
    """


class FluorescenceIntensity(Function):
    """The allowed input signatures of FluorescenceIntensity without optional
    arguments (kwargs) are:

    ``FluorescenceIntensity(Options, **kwargs)`` measures the fluorescence intensity data of the input samples.

    :param `**kwargs`: optional arguments for FluorescenceIntensity.
    :returns: UnitOperation - The unit operation that is to be used in sample/cell preparation.

    All optional parameters (kwargs) can be found in the 'Options' tab of the site: https://www.emeraldcloudlab.com/helpfiles/fluorescenceintensity.
    """


class FluorescenceKinetics(Function):
    """The allowed input signatures of FluorescenceKinetics without optional
    arguments (kwargs) are:

    ``FluorescenceKinetics(Options, **kwargs)`` measures the fluorescence kinetics data of the input samples.

    :param `**kwargs`: optional arguments for FluorescenceKinetics.
    :returns: UnitOperation - The unit operation that is to be used in sample/cell preparation.

    All optional parameters (kwargs) can be found in the 'Options' tab of the site: https://www.emeraldcloudlab.com/helpfiles/fluorescencekinetics.
    """


class FluorescencePolarizationKinetics(Function):
    """The allowed input signatures of FluorescencePolarizationKinetics without
    optional arguments (kwargs) are:

    ``FluorescencePolarizationKinetics(Options, **kwargs)`` measures the fluorescence polarization kinetics data of the input samples.

    :param `**kwargs`: optional arguments for FluorescencePolarizationKinetics.
    :returns: UnitOperation - The unit operation that is to be used in sample/cell preparation.

    All optional parameters (kwargs) can be found in the 'Options' tab of the site: https://www.emeraldcloudlab.com/helpfiles/fluorescencepolarizationkinetics.
    """


class FluorescencePolarization(Function):
    """The allowed input signatures of FluorescencePolarization without
    optional arguments (kwargs) are:

    ``FluorescencePolarization(Options, **kwargs)`` measures the fluorescence polarization data of the input samples.

    :param `**kwargs`: optional arguments for FluorescencePolarization.
    :returns: UnitOperation - The unit operation that is to be used in sample/cell preparation.

    All optional parameters (kwargs) can be found in the 'Options' tab of the site: https://www.emeraldcloudlab.com/helpfiles/fluorescencepolarization.
    """


class FluorescenceSpectroscopy(Function):
    """The allowed input signatures of FluorescenceSpectroscopy without
    optional arguments (kwargs) are:

    ``FluorescenceSpectroscopy(Options, **kwargs)`` measures the fluorescence spectroscopy data of the input samples.

    :param `**kwargs`: optional arguments for FluorescenceSpectroscopy.
    :returns: UnitOperation - The unit operation that is to be used in sample/cell preparation.

    All optional parameters (kwargs) can be found in the 'Options' tab of the site: https://www.emeraldcloudlab.com/helpfiles/fluorescencespectroscopy.
    """


class Grind(Function):
    """The allowed input signatures of Grind without optional arguments
    (kwargs) are:

    ``Grind(Options, **kwargs)`` reduces the size of powder particles by grinding solid substances into fine powders via a grinder (mill).

    :param `**kwargs`: optional arguments for Grind.
    :returns: UnitOperation - The unit operation that is to be used in sample/cell preparation.

    All optional parameters (kwargs) can be found in the 'Options' tab of the site: https://www.emeraldcloudlab.com/helpfiles/grind.
    """


class GrowCrystal(Function):
    """The allowed input signatures of GrowCrystal without optional arguments
    (kwargs) are:

    ``GrowCrystal(Options, **kwargs)`` prepares crystallization plate designed to grow crystals, and incubate and image the prepared crystallization plate.

    :param `**kwargs`: optional arguments for GrowCrystal.
    :returns: UnitOperation - The unit operation that is to be used in sample/cell preparation.

    All optional parameters (kwargs) can be found in the 'Options' tab of the site: https://www.emeraldcloudlab.com/helpfiles/growcrystal.
    """


class ICPMS(Function):
    """The allowed input signatures of ICPMS without optional arguments
    (kwargs) are:

    ``ICPMS(Options, **kwargs)`` atomize, ionize and analyze the elemental composition of the input analyte.

    :param `**kwargs`: optional arguments for ICPMS.
    :returns: UnitOperation - The unit operation that is to be used in sample/cell preparation.

    All optional parameters (kwargs) can be found in the 'Options' tab of the site: https://www.emeraldcloudlab.com/helpfiles/icpms.
    """


class ImageCells(Function):
    """The allowed input signatures of ImageCells without optional arguments
    (kwargs) are:

    ``ImageCells(Options, **kwargs)`` acquire microscopic images from the samples.

    :param `**kwargs`: optional arguments for ImageCells.
    :returns: UnitOperation - The unit operation that is to be used in sample/cell preparation.

    All optional parameters (kwargs) can be found in the 'Options' tab of the site: https://www.emeraldcloudlab.com/helpfiles/imagecells.
    """


class IncubateCells(Function):
    """The allowed input signatures of IncubateCells without optional arguments
    (kwargs) are:

    ``IncubateCells(Options, **kwargs)`` incubate cell samples for a specified period of time and at a specified temperature, humidity, and carbon dioxide percentage.

    :param `**kwargs`: optional arguments for IncubateCells.
    :returns: UnitOperation - The unit operation that is to be used in sample/cell preparation.

    All optional parameters (kwargs) can be found in the 'Options' tab of the site: https://www.emeraldcloudlab.com/helpfiles/incubatecells.
    """


class Incubate(Function):
    """The allowed input signatures of Incubate without optional arguments
    (kwargs) are:

    ``Incubate(Sample, **kwargs)`` generates an ExperimentSampleManipulation-compatible 'primitive' that describes incubating and mixing a sample at a specified temperature and shaking rate for a specified amount of time.

    :param `**kwargs`: optional arguments for Incubate.
    :returns: None

    All optional parameters (kwargs) can be found in the 'Options' tab of the site: https://www.emeraldcloudlab.com/helpfiles/incubate.
    """


class InoculateLiquidMedia(Function):
    """The allowed input signatures of InoculateLiquidMedia without optional
    arguments (kwargs) are:

    ``InoculateLiquidMedia(Options, **kwargs)`` moves bacterial colonies growing on solid media or in liquid media to fresh liquid media.

    :param `**kwargs`: optional arguments for InoculateLiquidMedia.
    :returns: UnitOperation - The unit operation that is to be used in sample/cell preparation.

    All optional parameters (kwargs) can be found in the 'Options' tab of the site: https://www.emeraldcloudlab.com/helpfiles/inoculateliquidmedia.
    """


class LabelContainer(Function):
    """The allowed input signatures of LabelContainer without optional
    arguments (kwargs) are:

    ``LabelContainer(Options, **kwargs)`` generates an ExperimentSamplePreparation/ExperimentCellPreparation-compatible 'UnitOperation' that labels a container for use in other primitives.

    :param `**kwargs`: optional arguments for LabelContainer.
    :returns: UnitOperation - The primitive that represents this labeled container.

    All optional parameters (kwargs) can be found in the 'Options' tab of the site: https://www.emeraldcloudlab.com/helpfiles/labelcontainer.
    """


class LabelSample(Function):
    """The allowed input signatures of LabelSample without optional arguments
    (kwargs) are:

    ``LabelSample(Options, **kwargs)`` generates an ExperimentSamplePreparation/ExperimentCellPreparation-compatible 'UnitOperation' that labels a sample in a container for use in other primitives.

    :param `**kwargs`: optional arguments for LabelSample.
    :returns: UnitOperation - The primitive that represents this labeled sample.

    All optional parameters (kwargs) can be found in the 'Options' tab of the site: https://www.emeraldcloudlab.com/helpfiles/labelsample.
    """


class LiquidLiquidExtraction(Function):
    """The allowed input signatures of LiquidLiquidExtraction without optional
    arguments (kwargs) are:

    ``LiquidLiquidExtraction(Options, **kwargs)`` separates the aqueous and organic phases of given samples via pipette or phase separator, in order to isolate a target analyte that is more concentrated in either the aqueous or organic phase.

    :param `**kwargs`: optional arguments for LiquidLiquidExtraction.
    :returns: UnitOperation - The unit operation that is to be used in sample/cell preparation.

    All optional parameters (kwargs) can be found in the 'Options' tab of the site: https://www.emeraldcloudlab.com/helpfiles/liquidliquidextraction.
    """


class LuminescenceIntensity(Function):
    """The allowed input signatures of LuminescenceIntensity without optional
    arguments (kwargs) are:

    ``LuminescenceIntensity(Options, **kwargs)`` measures the luminescence intensity data of the input samples.

    :param `**kwargs`: optional arguments for LuminescenceIntensity.
    :returns: UnitOperation - The unit operation that is to be used in sample/cell preparation.

    All optional parameters (kwargs) can be found in the 'Options' tab of the site: https://www.emeraldcloudlab.com/helpfiles/luminescenceintensity.
    """


class LuminescenceKinetics(Function):
    """The allowed input signatures of LuminescenceKinetics without optional
    arguments (kwargs) are:

    ``LuminescenceKinetics(Options, **kwargs)`` measures the luminescence kinetics data of the input samples.

    :param `**kwargs`: optional arguments for LuminescenceKinetics.
    :returns: UnitOperation - The unit operation that is to be used in sample/cell preparation.

    All optional parameters (kwargs) can be found in the 'Options' tab of the site: https://www.emeraldcloudlab.com/helpfiles/luminescencekinetics.
    """


class LuminescenceSpectroscopy(Function):
    """The allowed input signatures of LuminescenceSpectroscopy without
    optional arguments (kwargs) are:

    ``LuminescenceSpectroscopy(Options, **kwargs)`` measures the luminescence spectroscopy data of the input samples.

    :param `**kwargs`: optional arguments for LuminescenceSpectroscopy.
    :returns: UnitOperation - The unit operation that is to be used in sample/cell preparation.

    All optional parameters (kwargs) can be found in the 'Options' tab of the site: https://www.emeraldcloudlab.com/helpfiles/luminescencespectroscopy.
    """


class LyseCells(Function):
    """The allowed input signatures of LyseCells without optional arguments
    (kwargs) are:

    ``LyseCells(Options, **kwargs)`` ruptures the cell membranes of a cell containing sample to enable extraction of cellular components.

    :param `**kwargs`: optional arguments for LyseCells.
    :returns: UnitOperation - The unit operation that is to be used in sample/cell preparation.

    All optional parameters (kwargs) can be found in the 'Options' tab of the site: https://www.emeraldcloudlab.com/helpfiles/lysecells.
    """


class MagneticBeadSeparation(Function):
    """The allowed input signatures of MagneticBeadSeparation without optional
    arguments (kwargs) are:

    ``MagneticBeadSeparation(Options, **kwargs)`` isolates targets from samples by using a magnetic field to separate superparamagnetic particles from suspensions.

    :param `**kwargs`: optional arguments for MagneticBeadSeparation.
    :returns: UnitOperation - The unit operation that is to be used in sample/cell preparation.

    All optional parameters (kwargs) can be found in the 'Options' tab of the site: https://www.emeraldcloudlab.com/helpfiles/magneticbeadseparation.
    """


class MeasureContactAngle(Function):
    """The allowed input signatures of MeasureContactAngle without optional
    arguments (kwargs) are:

    ``MeasureContactAngle(Options, **kwargs)`` measure the contact angle between fiber and wetting liquid.

    :param `**kwargs`: optional arguments for MeasureContactAngle.
    :returns: UnitOperation - The unit operation that is to be used in sample/cell preparation.

    All optional parameters (kwargs) can be found in the 'Options' tab of the site: https://www.emeraldcloudlab.com/helpfiles/measurecontactangle.
    """


class MeasureRefractiveIndex(Function):
    """The allowed input signatures of MeasureRefractiveIndex without optional
    arguments (kwargs) are:

    ``MeasureRefractiveIndex(Options, **kwargs)`` measure the refractive index of sample.

    :param `**kwargs`: optional arguments for MeasureRefractiveIndex.
    :returns: UnitOperation - The unit operation that is to be used in sample/cell preparation.

    All optional parameters (kwargs) can be found in the 'Options' tab of the site: https://www.emeraldcloudlab.com/helpfiles/measurerefractiveindex.
    """


class MicrowaveDigestion(Function):
    """The allowed input signatures of MicrowaveDigestion without optional
    arguments (kwargs) are:

    ``MicrowaveDigestion(Options, **kwargs)`` digest sample with microwave to ensure full solubility for subsequent analysis, especially for ICP-MS.

    :param `**kwargs`: optional arguments for MicrowaveDigestion.
    :returns: UnitOperation - The unit operation that is to be used in sample/cell preparation.

    All optional parameters (kwargs) can be found in the 'Options' tab of the site: https://www.emeraldcloudlab.com/helpfiles/microwavedigestion.
    """


class Mix(Function):
    """The allowed input signatures of Mix without optional arguments (kwargs)
    are:

    ``Mix(Sample, **kwargs)`` generates an ExperimentSampleManipulation-compatible 'primitive' that describes mixing a sample using bench-top instrumentation or by pipetting on a micro liquid handling robot.

    :param `**kwargs`: optional arguments for Mix.
    :returns: None

    All optional parameters (kwargs) can be found in the 'Options' tab of the site: https://www.emeraldcloudlab.com/helpfiles/mix.
    """


class NephelometryKinetics(Function):
    """The allowed input signatures of NephelometryKinetics without optional
    arguments (kwargs) are:

    ``NephelometryKinetics(Options, **kwargs)`` measures the nephelometry kinetics data of the input samples.

    :param `**kwargs`: optional arguments for NephelometryKinetics.
    :returns: UnitOperation - The unit operation that is to be used in sample/cell preparation.

    All optional parameters (kwargs) can be found in the 'Options' tab of the site: https://www.emeraldcloudlab.com/helpfiles/nephelometrykinetics.
    """


class Nephelometry(Function):
    """The allowed input signatures of Nephelometry without optional arguments
    (kwargs) are:

    ``Nephelometry(Options, **kwargs)`` measures the nephelometry data of the input samples.

    :param `**kwargs`: optional arguments for Nephelometry.
    :returns: UnitOperation - The unit operation that is to be used in sample/cell preparation.

    All optional parameters (kwargs) can be found in the 'Options' tab of the site: https://www.emeraldcloudlab.com/helpfiles/nephelometry.
    """


class PCR(Function):
    """The allowed input signatures of PCR without optional arguments (kwargs)
    are:

    ``PCR(Options, **kwargs)`` amplifies target sequences from nucleic acid samples.

    :param `**kwargs`: optional arguments for PCR.
    :returns: UnitOperation - The unit operation that is to be used in sample/cell preparation.

    All optional parameters (kwargs) can be found in the 'Options' tab of the site: https://www.emeraldcloudlab.com/helpfiles/pcr.
    """


class Pellet(Function):
    """The allowed input signatures of Pellet without optional arguments
    (kwargs) are:

    ``Pellet(pelletRules, **kwargs)`` generates an ExperimentSampleManipulation-compatible 'primitive' that describes pelleting a sample at a specified intensity for a specified amount of time.

    :param `**kwargs`: optional arguments for Pellet.
    :returns: None

    All optional parameters (kwargs) can be found in the 'Options' tab of the site: https://www.emeraldcloudlab.com/helpfiles/pellet.
    """


class PickColonies(Function):
    """The allowed input signatures of PickColonies without optional arguments
    (kwargs) are:

    ``PickColonies(Options, **kwargs)`` moves bacterial colonies growing on solid media to a new liquid or solid media.

    :param `**kwargs`: optional arguments for PickColonies.
    :returns: UnitOperation - The unit operation that is to be used in sample/cell preparation.

    All optional parameters (kwargs) can be found in the 'Options' tab of the site: https://www.emeraldcloudlab.com/helpfiles/pickcolonies.
    """


class Precipitate(Function):
    """The allowed input signatures of Precipitate without optional arguments
    (kwargs) are:

    ``Precipitate(Options, **kwargs)`` combines precipitating reagent with sample and separates the resulting precipitate and liquid phase.

    :param `**kwargs`: optional arguments for Precipitate.
    :returns: UnitOperation - The unit operation that is to be used in sample/cell preparation.

    All optional parameters (kwargs) can be found in the 'Options' tab of the site: https://www.emeraldcloudlab.com/helpfiles/precipitate.
    """


class Resuspend(Function):
    """The allowed input signatures of Resuspend without optional arguments
    (kwargs) are:

    ``Resuspend(resuspendRules, **kwargs)`` generates an ExperimentSampleManipulation-compatible 'primitive' that describes the resuspension of a sample in solvent.

    :param `**kwargs`: optional arguments for Resuspend.
    :returns: None

    All optional parameters (kwargs) can be found in the 'Options' tab of the site: https://www.emeraldcloudlab.com/helpfiles/resuspend.
    """


class SerialDilute(Function):
    """The allowed input signatures of SerialDilute without optional arguments
    (kwargs) are:

    ``SerialDilute(Options, **kwargs)`` transfers an amount of sample into a container and dilutes it with buffers as specified.

    :param `**kwargs`: optional arguments for SerialDilute.
    :returns: UnitOperation - The unit operation that is to be used in sample/cell preparation.

    All optional parameters (kwargs) can be found in the 'Options' tab of the site: https://www.emeraldcloudlab.com/helpfiles/serialdilute.
    """


class SolidPhaseExtraction(Function):
    """The allowed input signatures of SolidPhaseExtraction without optional
    arguments (kwargs) are:

    ``SolidPhaseExtraction(Sample, **kwargs)`` generates an ExperimentSampleManipulation-compatible 'primitive' that describes solid phase extraction a sample through a specified extraction cartridge by applying a specified pressure for a specified amount of time.

    :param `**kwargs`: optional arguments for SolidPhaseExtraction.
    :returns: None

    All optional parameters (kwargs) can be found in the 'Options' tab of the site: https://www.emeraldcloudlab.com/helpfiles/solidphaseextraction.
    """


class SpreadCells(Function):
    """The allowed input signatures of SpreadCells without optional arguments
    (kwargs) are:

    ``SpreadCells(Options, **kwargs)`` moves suspended colonies growing in liquid media to solid media and moves them across the surface of the media in a pattern to promote growth of the colonies.

    :param `**kwargs`: optional arguments for SpreadCells.
    :returns: UnitOperation - The unit operation that is to be used in sample/cell preparation.

    All optional parameters (kwargs) can be found in the 'Options' tab of the site: https://www.emeraldcloudlab.com/helpfiles/spreadcells.
    """


class StreakCells(Function):
    """The allowed input signatures of StreakCells without optional arguments
    (kwargs) are:

    ``StreakCells(Options, **kwargs)`` moves suspended colonies growing in liquid media to solid media and moves them across the surface of the media in a pattern to try and isolate individual colonies.

    :param `**kwargs`: optional arguments for StreakCells.
    :returns: UnitOperation - The unit operation that is to be used in sample/cell preparation.

    All optional parameters (kwargs) can be found in the 'Options' tab of the site: https://www.emeraldcloudlab.com/helpfiles/streakcells.
    """


class ThawCells(Function):
    """The allowed input signatures of ThawCells without optional arguments
    (kwargs) are:

    ``ThawCells(Options, **kwargs)`` thaw a frozen vial of cells for use in downstream cell culturing.

    :param `**kwargs`: optional arguments for ThawCells.
    :returns: UnitOperation - The unit operation that is to be used in sample/cell preparation.

    All optional parameters (kwargs) can be found in the 'Options' tab of the site: https://www.emeraldcloudlab.com/helpfiles/thawcells.
    """


class Transfer(Function):
    """The allowed input signatures of Transfer without optional arguments
    (kwargs) are:

    ``Transfer(transferRules, **kwargs)`` generates an ExperimentSampleManipulation-compatible 'primitive' that describes a transfer of a source to a destination.

    :param `**kwargs`: optional arguments for Transfer.
    :returns: None

    All optional parameters (kwargs) can be found in the 'Options' tab of the site: https://www.emeraldcloudlab.com/helpfiles/transfer.
    """


class Uncover(Function):
    """The allowed input signatures of Uncover without optional arguments
    (kwargs) are:

    ``Uncover(Sample, **kwargs)`` generates an ExperimentSampleManipulation-compatible 'primitive' that describes removing a lid from a plate.

    :param `**kwargs`: optional arguments for Uncover.
    :returns: None

    All optional parameters (kwargs) can be found in the 'Options' tab of the site: https://www.emeraldcloudlab.com/helpfiles/uncover.
    """


class VisualInspection(Function):
    """The allowed input signatures of VisualInspection without optional
    arguments (kwargs) are:

    ``VisualInspection(Options, **kwargs)`` records a video of a sample container as it is agitated on a shaker/vortex.

    :param `**kwargs`: optional arguments for VisualInspection.
    :returns: UnitOperation - The unit operation that is to be used in sample/cell preparation.

    All optional parameters (kwargs) can be found in the 'Options' tab of the site: https://www.emeraldcloudlab.com/helpfiles/visualinspection.
    """


class Wait(Function):
    """The allowed input signatures of Wait without optional arguments (kwargs)
    are:

    ``Wait(duration, **kwargs)`` generates an ExperimentSampleManipulation-compatible 'primitive' that describes the pausing of a specified duration.

    :param `**kwargs`: optional arguments for Wait.
    :returns: None

    All optional parameters (kwargs) can be found in the 'Options' tab of the site: https://www.emeraldcloudlab.com/helpfiles/wait.
    """


class WashCells(Function):
    """The allowed input signatures of WashCells without optional arguments
    (kwargs) are:

    ``WashCells(washCellsRules, **kwargs)`` generates an ExperimentRoboticCellPreparation-compatible 'primitive' that describes a wash cells process.

    :param `**kwargs`: optional arguments for WashCells.
    :returns: None

    All optional parameters (kwargs) can be found in the 'Options' tab of the site: https://www.emeraldcloudlab.com/helpfiles/washcells.
    """
